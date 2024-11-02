from prefect import flow
from prefect.tasks import task_input_hash
from datetime import timedelta
import yaml
import os
from typing import Dict, Any

from ..tasks.extract_tasks import extract_from_postgres, extract_from_s3
from ..tasks.transform_tasks import clean_data, transform_data
from ..tasks.data_quality import validate_data_quality, check_data_freshness

@flow(
    name="main_data_pipeline",
    description="Main data processing pipeline",
    version="1.0.0"
)
async def main_data_pipeline(
    params: Dict[str, Any] = None
) -> None:
    """主数据处理流程"""
    
    # 加载配置
    config_path = os.path.join(
        os.path.dirname(__file__), 
        '../config/prefect_config.yml'
    )
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    try:
        # 1. 提取数据
        postgres_data = await extract_from_postgres(
            query="SELECT * FROM source_table",
            connection_params=config['source']['postgres']
        )
        
        s3_data = await extract_from_s3(
            bucket=config['source']['s3']['bucket'],
            key="raw_data/latest.parquet"
        )
        
        # 2. 检查数据新鲜度
        await check_data_freshness(
            data=postgres_data,
            timestamp_column='created_at',
            max_delay_hours=24
        )
        
        # 3. 数据清洗
        clean_postgres_data = await clean_data(postgres_data)
        clean_s3_data = await clean_data(s3_data)
        
        # 4. 数据转换
        transformed_data = await transform_data(
            df=clean_postgres_data,
            transformations=config['transformations']
        )
        
        # 5. 数据质量验证
        validation_results = await validate_data_quality(
            data=transformed_data,
            expectations_suite="production_suite"
        )
        
        return {
            "status": "success",
            "validation_results": validation_results,
            "records_processed": len(transformed_data)
        }
        
    except Exception as e:
        # 发送失败通知
        await send_failure_notification(str(e))
        raise

@flow(
    name="scheduled_pipeline",
    schedule=timedelta(hours=1)
)
async def scheduled_pipeline():
    """定时执行的管道"""
    return await main_data_pipeline()

if __name__ == "__main__":
    # 本地执行
    import asyncio
    asyncio.run(main_data_pipeline())
