from .base_processor import BaseProcessor
import pandas as pd
import numpy as np

class CleaningProcessor(BaseProcessor):
    """数据清洗处理器"""
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 处理重复值
        if self.config.get('remove_duplicates', True):
            df = df.drop_duplicates()
            
        # 处理缺失值
        for col, strategy in self.config.get('null_handling', {}).items():
            if strategy == 'drop':
                df = df.dropna(subset=[col])
            elif strategy == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == 'median':
                df[col] = df[col].fillna(df[col].median())
            elif strategy == 'mode':
                df[col] = df[col].fillna(df[col].mode()[0])
            elif isinstance(strategy, (int, float, str)):
                df[col] = df[col].fillna(strategy)
                
        # 处理异常值
        for col, limits in self.config.get('outlier_handling', {}).items():
            if limits.get('method') == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                df[col] = df[col].clip(lower=lower, upper=upper)
                
        return df
