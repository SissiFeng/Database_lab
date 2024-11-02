from typing import Dict, Any
import logging
from datetime import datetime, timezone

class LifecycleManager:
    def __init__(self, s3_client: Any, config: Dict[str, Any]):
        self.s3_client = s3_client
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def apply_rules(self) -> None:
        """应用生命周期规则"""
        try:
            lifecycle_rules = []
            
            # 构建生命周期规则
            for category, rules in self.config['cost_optimization']['lifecycle_rules'].items():
                lifecycle_rule = self._build_lifecycle_rule(category, rules)
                lifecycle_rules.append(lifecycle_rule)
            
            # 应用规则到存储桶
            await self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.config['bucket_name'],
                LifecycleConfiguration={'Rules': lifecycle_rules}
            )
            
        except Exception as e:
            self.logger.error(f"Failed to apply lifecycle rules: {e}")

    def _build_lifecycle_rule(self, category: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """构建生命周期规则"""
        rule = {
            'ID': f'{category}_lifecycle_rule',
            'Status': 'Enabled',
            'Filter': {'Prefix': f'{category}/'},
            'Transitions': [],
            'Expiration': {'Days': rules['expiration_days']}
        }
        
        # 添加转换规则
        for transition in rules['transition_schedule']:
            rule['Transitions'].append({
                'Days': transition['days'],
                'StorageClass': transition['storage_class']
            })
        
        return rule

    async def cleanup_expired_objects(self) -> None:
        """清理过期对象"""
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            async for page in paginator.paginate(Bucket=self.config['bucket_name']):
                for obj in page.get('Contents', []):
                    await self._check_and_cleanup_object(obj)
                    
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")

    async def _check_and_cleanup_object(self, obj: Dict[str, Any]) -> None:
        """检查并清理单个对象"""
        try:
            # 获取对象元数据
            response = await self.s3_client.head_object(
                Bucket=self.config['bucket_name'],
                Key=obj['Key']
            )
            
            # 检查是否过期
            last_modified = response['LastModified']
            age_days = (datetime.now(timezone.utc) - last_modified).days
            
            # 根据规则决定是否删除
            for category, rules in self.config['cost_optimization']['lifecycle_rules'].items():
                if obj['Key'].startswith(f'{category}/'):
                    if age_days > rules['expiration_days']:
                        await self.s3_client.delete_object(
                            Bucket=self.config['bucket_name'],
                            Key=obj['Key']
                        )
                        self.logger.info(f"Deleted expired object: {obj['Key']}")
                    break
                    
        except Exception as e:
            self.logger.error(f"Failed to check/cleanup object {obj['Key']}: {e}")
