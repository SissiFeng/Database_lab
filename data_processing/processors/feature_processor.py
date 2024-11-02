from .base_processor import BaseProcessor
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class TransformProcessor(BaseProcessor):
    """数据转换处理器"""
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 数据类型转换
        for col, dtype in self.config.get('dtype_mapping', {}).items():
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                self.logger.error(f"Type conversion failed for {col}: {str(e)}")
                
        # 特征缩放
        for col, method in self.config.get('scaling', {}).items():
            if method == 'standard':
                scaler = StandardScaler()
                df[col] = scaler.fit_transform(df[[col]])
            elif method == 'minmax':
                scaler = MinMaxScaler()
                df[col] = scaler.fit_transform(df[[col]])
                
        # 特征编码
        for col, method in self.config.get('encoding', {}).items():
            if method == 'onehot':
                df = pd.get_dummies(df, columns=[col], prefix=col)
            elif method == 'label':
                df[col] = df[col].astype('category').cat.codes
                
        return df
