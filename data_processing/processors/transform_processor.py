from .base_processor import BaseProcessor
import pandas as pd
import numpy as np

class FeatureProcessor(BaseProcessor):
    """特征工程处理器"""
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 特征组合
        for feature in self.config.get('feature_combinations', []):
            cols = feature['columns']
            method = feature['method']
            name = feature['name']
            
            if method == 'multiply':
                df[name] = df[cols].prod(axis=1)
            elif method == 'divide':
                df[name] = df[cols[0]] / df[cols[1]]
            elif method == 'add':
                df[name] = df[cols].sum(axis=1)
            elif method == 'subtract':
                df[name] = df[cols[0]] - df[cols[1]]
                
        # 时间特征提取
        for col in self.config.get('datetime_features', []):
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[f'{col}_year'] = df[col].dt.year
                df[f'{col}_month'] = df[col].dt.month
                df[f'{col}_day'] = df[col].dt.day
                df[f'{col}_hour'] = df[col].dt.hour
                df[f'{col}_dayofweek'] = df[col].dt.dayofweek
                
        # 窗口特征
        for feature in self.config.get('window_features', []):
            col = feature['column']
            window = feature['window']
            operations = feature['operations']
            
            for op in operations:
                if op == 'mean':
                    df[f'{col}_mean_{window}'] = df[col].rolling(window).mean()
                elif op == 'std':
                    df[f'{col}_std_{window}'] = df[col].rolling(window).std()
                elif op == 'min':
                    df[f'{col}_min_{window}'] = df[col].rolling(window).min()
                elif op == 'max':
                    df[f'{col}_max_{window}'] = df[col].rolling(window).max()
                    
        return df
