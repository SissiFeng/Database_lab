from prefect import task
from prefect.tasks.database.postgres import PostgresExecute
from prefect.tasks.aws import S3Download
import pandas as pd
from typing import Dict, Any

@task(
    name="extract_from_postgres",
    retry_delay_seconds=30,
    max_retries=3,
    tags=["extract", "postgres"]
)
async def extract_from_postgres(
    query: str,
    connection_params: Dict[str, Any]
) -> pd.DataFrame:
    """从PostgreSQL提取数据"""
    
    postgres_task = PostgresExecute(
        **connection_params,
        task_name="postgres_extract"
    )
    
    result = await postgres_task.run(query=query)
    return pd.DataFrame(result)

@task(
    name="extract_from_s3",
    retry_delay_seconds=30,
    max_retries=3,
    tags=["extract", "s3"]
)
async def extract_from_s3(
    bucket: str,
    key: str,
    file_format: str = "parquet"
) -> pd.DataFrame:
    """从S3提取数据"""
    
    s3_task = S3Download(
        bucket=bucket,
        task_name="s3_extract"
    )
    
    local_path = await s3_task.run(key=key)
    
    if file_format == "parquet":
        return pd.read_parquet(local_path)
    elif file_format == "csv":
        return pd.read_csv(local_path)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
