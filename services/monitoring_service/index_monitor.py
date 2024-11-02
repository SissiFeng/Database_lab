from utils.index_advisor.index_analyzer import QueryIndexAdvisor
import logging
import schedule
import time
from datetime import datetime
import json

class IndexMonitorService:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)
            
        self.advisor = QueryIndexAdvisor(self.config['database_url'])
        self.logger = logging.getLogger(__name__)

    def start_monitoring(self):
        """启动索引监控服务"""
        # 设置定期任务
        schedule.every().day.at("00:00").do(self.analyze_indexes)
        
        while True:
            schedule.run_pending()
            time.sleep(3600)  # 每小时检查一次

    def analyze_indexes(self):
        """分析并优化索引"""
        try:
            # 收集查询模式
            self.advisor.collect_query_patterns(self.config['query_log_path'])
            
            # 获取索引建议
            recommendations = self.advisor.recommend_indexes()
            
            # 评估影响
            impact_analysis = self.advisor.evaluate_index_impact(recommendations)
            
            # 记录建议
            self._log_recommendations(recommendations, impact_analysis)
            
            # 如果配置了自动执行，执行索引创建
            if self.config.get('auto_execute', False):
                self._execute_recommendations(recommendations, impact_analysis)
                
        except Exception as e:
            self.logger.error(f"Error in index analysis: {e}")

    def _log_recommendations(self, recommendations, impact_analysis):
        """记录索引建议"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"index_recommendations_{timestamp}.json"
        
        with open(log_file, 'w') as f:
            json.dump({
                'recommendations': recommendations,
                'impact_analysis': impact_analysis,
                'timestamp': timestamp
            }, f, indent=2)

    def _execute_recommendations(self, recommendations, impact_analysis):
        """执行索引建议"""
        for rec, impact in zip(recommendations, impact_analysis):
            if self._should_implement_index(impact):
                try:
                    # 执行创建索引
                    self._create_index(rec)
                    self.logger.info(f"Created index: {rec}")
                except Exception as e:
                    self.logger.error(f"Error creating index: {e}")

    def _should_implement_index(self, impact_analysis):
        """决定是否应该实施某个索引建议"""
        # 设置阈值
        MIN_PERFORMANCE_GAIN = 0.1  # 10%的性能提升
        MAX_SIZE_IMPACT = 0.05      # 5%的存储影响
        
        return (impact_analysis['estimated_performance_gain'] > MIN_PERFORMANCE_GAIN and
                impact_analysis['estimated_size'] < MAX_SIZE_IMPACT)
