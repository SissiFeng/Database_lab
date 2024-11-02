from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
from datetime import datetime

class BaseTransformer(ABC):
    """数据转换器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    async def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """转换数据的抽象方法"""
        pass
        
    async def validate_schema(self, data: List[Dict[str, Any]]) -> bool:
        """验证数据模式"""
        return True
        
    async def _handle_null_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理空值"""
        if self.config['transformations']['null_handling'] == 'drop':
            return {k: v for k, v in data.items() if v is not None}
        return data
        
    async def _format_dates(self, date_str: str) -> datetime:
        """格式化日期"""
        try:
            return datetime.strptime(
                date_str, 
                self.config['transformations']['date_format']
            )
        except ValueError as e:
            self.logger.error(f"Date format error: {str(e)}")
            raise
