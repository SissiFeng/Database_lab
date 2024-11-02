from prefect import task
import pandas as pd
from typing import List, Dict, Any

@task(
    name="clean_data",
    tags=["transform"]
)
async def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """数据清洗任务"""
    # 删除重复行
    df = df.drop_duplicates()
    
    # 处理缺失值
    df = df.dropna(subset=['id'])  # 必需字段
    df = df.fillna({
        'numeric_col': 0,
        'string_col': 'unknown'
    })
    
    return df

@task(
    name="transform_data",
    tags=["transform"]
)
async def transform_data(
    df: pd.DataFrame,
    transformations: List[Dict[str, Any]]
) -> pd.DataFrame:
    """数据转换任务"""
    for transform in transformations:
        if transform['type'] == 'rename':
            df = df.rename(columns=transform['mapping'])
        elif transform['type'] == 'calculate':
            df[transform['target']] = df.eval(transform['formula'])
        elif transform['type'] == 'aggregate':
            df = df.groupby(transform['group_by']).agg(transform['aggregations'])
            
    return df
