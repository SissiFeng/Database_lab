from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
from datetime import datetime
import yaml
import os

class BasePipeline(ABC):
    """ETL管道基类"""
    
    def __init__(self, pipeline_id: str, config_path: str = None):
        self.pipeline_id = pipeline_id
        self.start_time = None
        self.end_time = None
        self.status = "initialized"
        self.metrics = {}
        
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 设置日志
        self.logger = self._setup_logger()
        
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """加载ETL配置"""
        if not config_path:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                '../config/etl_config.yml'
            )
            
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
            
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(f"etl.pipeline.{self.pipeline_id}")
        
        # 设置日志级别
        logger.setLevel(self.config['logging']['level'])
        
        # 添加处理器
        for handler_config in self.config['logging']['handlers']:
            if handler_config['type'] == 'console':
                handler = logging.StreamHandler()
            elif handler_config['type'] == 'file':
                handler = logging.RotatingFileHandler(
                    filename=handler_config['filename'],
                    maxBytes=handler_config['max_bytes'],
                    backupCount=handler_config['backup_count']
                )
            
            formatter = logging.Formatter(self.config['logging']['format'])
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    async def execute(self) -> bool:
        """执行ETL管道"""
        try:
            self.start_time = datetime.now()
            self.status = "running"
            self.logger.info(f"Starting pipeline: {self.pipeline_id}")
            
            # 验证配置
            await self.validate_config()
            
            # 执行提取
            data = await self.extract()
            self.logger.info(f"Extracted {len(data)} records")
            
            # 执行转换
            transformed_data = await self.transform(data)
            self.logger.info(f"Transformed {len(transformed_data)} records")
            
            # 执行加载
            await self.load(transformed_data)
            self.logger.info("Data loaded successfully")
            
            self.status = "completed"
            self.end_time = datetime.now()
            
            # 记录指标
            self._record_metrics()
            
            return True
            
        except Exception as e:
            self.status = "failed"
            self.end_time = datetime.now()
            self.logger.error(f"Pipeline failed: {str(e)}")
            await self._handle_failure(e)
            return False
            
    @abstractmethod
    async def validate_config(self) -> bool:
        """验证管道配置"""
        pass
        
    @abstractmethod
    async def extract(self) -> List[Dict[str, Any]]:
        """从数据源提取数据"""
        pass
        
    @abstractmethod
    async def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """转换数据"""
        pass
        
    @abstractmethod
    async def load(self, data: List[Dict[str, Any]]) -> bool:
        """加载数据到目标"""
        pass
        
    async def _handle_failure(self, error: Exception) -> None:
        """处理管道失败"""
        # 发送��警
        await self._send_alerts(error)
        
        # 清理资源
        await self._cleanup()
        
    async def _send_alerts(self, error: Exception) -> None:
        """发送告警通知"""
        if self.config['monitoring']['alerts']['email']['enabled']:
            await self._send_email_alert(error)
            
        if self.config['monitoring']['alerts']['slack']['enabled']:
            await self._send_slack_alert(error)
            
    def _record_metrics(self) -> None:
        """记录管道指标"""
        self.metrics.update({
            'pipeline_id': self.pipeline_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': (self.end_time - self.start_time).total_seconds(),
            'status': self.status,
            'records_processed': self.records_processed
        })
        
    async def _cleanup(self) -> None:
        """清理资源"""
        pass
