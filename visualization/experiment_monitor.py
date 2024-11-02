import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import numpy as np
from datetime import datetime, timedelta

class ExperimentMonitor:
    def __init__(self):
        self.interface = self.create_interface()
    
    def create_interface(self) -> gr.Blocks:
        """创建监控界面"""
        with gr.Blocks(theme=gr.themes.Soft()) as interface:
            gr.Markdown("## 实验监控面板")
            
            with gr.Row():
                # 左侧控制面板
                with gr.Column(scale=1):
                    date_range = gr.DateRange(
                        label="日期范围",
                        value=[
                            datetime.now() - timedelta(days=7),
                            datetime.now()
                        ]
                    )
                    experiment_dropdown = gr.Dropdown(
                        choices=self.get_experiment_list(),
                        label="选择实验",
                        multiselect=True
                    )
                    refresh_btn = gr.Button("刷新数据")
            
            with gr.Row():
                # 关键指标展示
                with gr.Column(scale=1):
                    success_rate = gr.Number(
                        label="实验成功率",
                        value=0.0,
                        format="%.2f%%"
                    )
                with gr.Column(scale=1):
                    avg_duration = gr.Number(
                        label="平均实验时长",
                        value=0.0,
                        format="%.2f min"
                    )
                with gr.Column(scale=1):
                    total_samples = gr.Number(
                        label="样本总数",
                        value=0
                    )
            
            with gr.Row():
                # 图表展示
                with gr.Column(scale=2):
                    success_trend_plot = gr.Plot(label="成功率趋势")
                with gr.Column(scale=2):
                    duration_box_plot = gr.Plot(label="实验时长分布")
            
            with gr.Row():
                with gr.Column():
                    metrics_table = gr.DataFrame(
                        label="详细指标",
                        headers=["实验ID", "状态", "开始时间", "结束时间", "样本数", "成功率"]
                    )
            
            # 事件处理
            refresh_btn.click(
                fn=self.update_dashboard,
                inputs=[date_range, experiment_dropdown],
                outputs=[
                    success_rate,
                    avg_duration,
                    total_samples,
                    success_trend_plot,
                    duration_box_plot,
                    metrics_table
                ]
            )
            
        return interface
    
    def get_experiment_list(self) -> List[str]:
        """获取实验列表"""
        # 这里应该从数据库获取实验列表
        return ["Experiment_A", "Experiment_B", "Experiment_C"]
    
    def update_dashboard(
        self,
        date_range: List[datetime],
        selected_experiments: List[str]
    ) -> tuple:
        """更新仪表板数据"""
        # 获取数据
        df = self.fetch_experiment_data(date_range, selected_experiments)
        
        # 计算关键指标
        success_rate_val = self.calculate_success_rate(df)
        avg_duration_val = self.calculate_avg_duration(df)
        total_samples_val = len(df)
        
        # 生成图表
        success_trend = self.create_success_trend_plot(df)
        duration_box = self.create_duration_box_plot(df)
        
        # 生成详细指标表
        metrics_df = self.create_metrics_table(df)
        
        return (
            success_rate_val,
            avg_duration_val,
            total_samples_val,
            success_trend,
            duration_box,
            metrics_df
        )
    
    def fetch_experiment_data(
        self,
        date_range: List[datetime],
        selected_experiments: List[str]
    ) -> pd.DataFrame:
        """获取实验数据"""
        # 这里应该从数据库获取实验数据
        # 示例数据
        data = {
            'experiment_id': np.random.choice(selected_experiments, 100),
            'status': np.random.choice(['success', 'failed'], 100, p=[0.8, 0.2]),
            'start_time': [
                date_range[0] + timedelta(
                    hours=np.random.randint(0, 24*7)
                ) for _ in range(100)
            ],
            'duration': np.random.normal(60, 10, 100),  # 分钟
            'sample_count': np.random.randint(10, 100, 100)
        }
        return pd.DataFrame(data)
    
    def create_success_trend_plot(self, df: pd.DataFrame) -> go.Figure:
        """创建成功率趋势图"""
        daily_success = df.groupby(
            df['start_time'].dt.date
        )['status'].apply(
            lambda x: (x == 'success').mean() * 100
        ).reset_index()
        
        fig = px.line(
            daily_success,
            x='start_time',
            y='status',
            title='实验成功率趋势',
            labels={'status': '成功率 (%)', 'start_time': '日期'}
        )
        return fig
    
    def create_duration_box_plot(self, df: pd.DataFrame) -> go.Figure:
        """创建实验时长分布图"""
        fig = px.box(
            df,
            x='experiment_id',
            y='duration',
            title='实验时长分布',
            labels={'duration': '时长 (分钟)', 'experiment_id': '实验'}
        )
        return fig
    
    def create_metrics_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """创建指标表"""
        metrics = df.groupby('experiment_id').agg({
            'status': lambda x: (x == 'success').mean() * 100,
            'start_time': 'min',
            'start_time': 'max',
            'sample_count': 'sum'
        }).reset_index()
        
        metrics.columns = ['实验ID', '成功率', '开始时间', '结束时间', '样本数']
        return metrics

    def launch(self, share: bool = False):
        """启动监控界面"""
        self.interface.launch(share=share)

if __name__ == "__main__":
    monitor = ExperimentMonitor()
    monitor.launch()
