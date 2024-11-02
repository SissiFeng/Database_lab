import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.monitoring_service.index_monitor import IndexMonitorService

def main():
    config_path = project_root / 'config' / 'index_monitor.json'
    
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    
    try:
        monitor = IndexMonitorService(str(config_path))
        monitor.start_monitoring()
    except Exception as e:
        print(f"Error starting monitor service: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()