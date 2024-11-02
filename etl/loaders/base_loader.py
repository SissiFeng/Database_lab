from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

class BaseLoader(ABC):
    """数据加载器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    async def load(self, data: List[Dict[str, Any]]) -> bool:
        """加载数据的抽象方法"""
        pass
        
    @abstractmethod
    async def validate_destination(self) -> bool:
        """验证目标位置"""
        pass
        
    async def _batch_data(self, data: List[Dict[str, Any]], batch_size: int) -> List[List[Dict[str, Any]]]:
        """将数据分批"""
        return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
        
    async def _handle_load_error(self, error: Exception, batch: List[Dict[str, Any]]) -> None:
        """处理加载错误"""
        self.logger.error(f"Loading error: {str(error)}")
        # 可以实现重试逻辑
        raise error
