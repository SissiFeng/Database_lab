from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import logging

class BaseProcessor(ABC):
    """数据处理基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """处理数据的抽象方法"""
        pass
        
    def validate_input(self, data: pd.DataFrame) -> bool:
        """验证输入数据"""
        return True

class DataProcessor:
    """数据处理管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.processors = []
        
    def add_processor(self, processor: BaseProcessor) -> None:
        """添加处理器"""
        self.processors.append(processor)
        
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """执行所有处理步骤"""
        processed_data = data.copy()
        for processor in self.processors:
            try:
                if processor.validate_input(processed_data):
                    processed_data = processor.process(processed_data)
                else:
                    self.logger.error(f"Validation failed for {processor.__class__.__name__}")
            except Exception as e:
                self.logger.error(f"Processing failed: {str(e)}")
                raise
                
        return processed_data
