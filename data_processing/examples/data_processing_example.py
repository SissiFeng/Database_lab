from data_processing.processors import (
    DataProcessor,
    CleaningProcessor,
    TransformProcessor,
    FeatureProcessor
)
import pandas as pd

# 配置
config = {
    'cleaning': {
        'remove_duplicates': True,
        'null_handling': {
            'numeric_col': 'mean',
            'categorical_col': 'mode',
            'required_col': 'drop'
        },
        'outlier_handling': {
            'numeric_col': {'method': 'iqr'}
        }
    },
    'transform': {
        'dtype_mapping': {
            'categorical_col': 'category',
            'date_col': 'datetime64[ns]'
        },
        'scaling': {
            'numeric_col': 'standard'
        },
        'encoding': {
            'categorical_col': 'onehot'
        }
    },
    'feature': {
        'feature_combinations': [
            {
                'name': 'feature_product',
                'columns': ['col1', 'col2'],
                'method': 'multiply'
            }
        ],
        'datetime_features': ['date_col'],
        'window_features': [
            {
                'column': 'numeric_col',
                'window': 7,
                'operations': ['mean', 'std']
            }
        ]
    }
}

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """处理数据"""
    # 创建处理器
    processor = DataProcessor(config)
    
    # 添加处理步骤
    processor.add_processor(CleaningProcessor(config['cleaning']))
    processor.add_processor(TransformProcessor(config['transform']))
    processor.add_processor(FeatureProcessor(config['feature']))
    
    # 执行处理
    return processor.process(data)

if __name__ == "__main__":
    # 示例数据
    data = pd.read_csv('data.csv')
    
    # 处理数据
    processed_data = process_data(data)
    print("处理完成！")
    print(f"原始数据形状: {data.shape}")
    print(f"处理后数据形状: {processed_data.shape}")
