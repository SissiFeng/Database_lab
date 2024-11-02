from prefect import task
from typing import Dict, List, Any
import pandas as pd
import great_expectations as ge

@task(
    name="validate_data_quality",
    retry_delay_seconds=60,
    max_retries=3,
    tags=["validation"]
)
async def validate_data_quality(
    data: pd.DataFrame,
    expectations_suite: str
) -> Dict[str, Any]:
    """数据质量验证任务"""
    
    context = ge.data_context.DataContext()
    
    # 创建期望套件
    suite = context.get_expectation_suite(expectations_suite)
    
    # 验证数据
    validator = ge.dataset.PandasDataset(
        data,
        expectation_suite=suite
    )
    
    results = validator.validate()
    
    if not results["success"]:
        raise ValueError(f"Data quality validation failed: {results}")
        
    return results

@task(
    name="check_data_freshness",
    tags=["monitoring"]
)
async def check_data_freshness(
    data: pd.DataFrame,
    timestamp_column: str,
    max_delay_hours: int = 24
) -> bool:
    """检查数据新鲜度"""
    latest_timestamp = pd.to_datetime(data[timestamp_column]).max()
    current_time = pd.Timestamp.now()
    delay = (current_time - latest_timestamp).total_seconds() / 3600
    
    if delay > max_delay_hours:
        raise ValueError(f"Data is too old: {delay} hours behind")
        
    return True
