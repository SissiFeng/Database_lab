import boto3
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .storage_optimizer import StorageOptimizer
from .performance_monitor import PerformanceMonitor
from .lifecycle_manager import LifecycleManager

class S3Manager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['region']
        )
        
        # 初始化子模块
        self.storage_optimizer = StorageOptimizer(self.s3_client, config)
        self.performance_monitor = PerformanceMonitor(self.s3_client, config)
        self.lifecycle_manager = LifecycleManager(self.s3_client, config)
        
        self.logger = logging.getLogger(__name__)

    async def upload_file(self, local_path: str, s3_key: str) -> bool:
        """智能上传文件"""
        try:
            # 获取最优上传策略
            upload_strategy = await self.storage_optimizer.get_upload_strategy(
                local_path, s3_key
            )
            
            # 执行上传
            if upload_strategy['multipart']:
                await self._multipart_upload(local_path, s3_key, upload_strategy)
            else:
                await self._simple_upload(local_path, s3_key, upload_strategy)
            
            # 应用存储策略
            await self.storage_optimizer.apply_storage_class(s3_key)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            return False

    async def _multipart_upload(self, local_path: str, s3_key: str, 
                              strategy: Dict[str, Any]) -> None:
        """分片上传实现"""
        file_size = Path(local_path).stat().st_size
        part_size = strategy['part_size']
        
        # 初始化分片上传
        response = await self.s3_client.create_multipart_upload(
            Bucket=self.config['bucket_name'],
            Key=s3_key,
            StorageClass=strategy['storage_class']
        )
        
        upload_id = response['UploadId']
        parts = []
        
        try:
            with open(local_path, 'rb') as file:
                part_number = 1
                while True:
                    data = file.read(part_size)
                    if not data:
                        break
                        
                    # 上传分片
                    response = await self.s3_client.upload_part(
                        Bucket=self.config['bucket_name'],
                        Key=s3_key,
                        UploadId=upload_id,
                        PartNumber=part_number,
                        Body=data
                    )
                    
                    parts.append({
                        'PartNumber': part_number,
                        'ETag': response['ETag']
                    })
                    part_number += 1
            
            # 完成分片上传
            await self.s3_client.complete_multipart_upload(
                Bucket=self.config['bucket_name'],
                Key=s3_key,
                UploadId=upload_id,
                MultipartUpload={'Parts': parts}
            )
            
        except Exception as e:
            # 取消分片上传
            await self.s3_client.abort_multipart_upload(
                Bucket=self.config['bucket_name'],
                Key=s3_key,
                UploadId=upload_id
            )
            raise e

    async def download_file(self, s3_key: str, local_path: str) -> bool:
        """智能下载文件"""
        try:
            # 获取下载策略
            download_strategy = await self.storage_optimizer.get_download_strategy(s3_key)
            
            # 执行下载
            await self.s3_client.download_file(
                self.config['bucket_name'],
                s3_key,
                local_path,
                Config=download_strategy['config']
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            return False

    async def optimize_storage(self) -> None:
        """执行存储优化"""
        await self.storage_optimizer.optimize()

    async def monitor_performance(self) -> Dict[str, Any]:
        """获取性能监控数据"""
        return await self.performance_monitor.get_metrics()

    async def manage_lifecycle(self) -> None:
        """管理对象生命周期"""
        await self.lifecycle_manager.apply_rules()
