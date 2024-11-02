from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging

class BaseExtractor(ABC):
    """数据提取器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    async def extract(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """提取数据的抽象方法"""
        pass
        
    @abstractmethod
    async def validate_source(self) -> bool:
        """验证数据源的抽象方法"""
        pass
        
    async def _handle_extraction_error(self, error: Exception) -> None:
        """处理提取错误"""
        self.logger.error(f"Extraction error: {str(error)}")
        raise error
        
    async def _validate_params(self, params: Optional[Dict[str, Any]]) -> bool:
        """验证提取参数"""
        return True
