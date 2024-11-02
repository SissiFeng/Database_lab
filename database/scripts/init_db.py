import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DATABASE_CONFIG

def init_database():
    """初始化数据库"""
    # 连接到默认的postgres数据库
    conn = psycopg2.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database='postgres'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # 创建数据库（如果不存在）
    try:
        cur.execute(f"CREATE DATABASE {DATABASE_CONFIG['database']}")
    except psycopg2.Error as e:
        print(f"Database already exists or error: {e}")
    
    # 关闭postgres连接
    cur.close()
    conn.close()
    
    # 连接到新创建的数据库
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    # 执行所有SQL文件
    schema_dir = os.path.join(os.path.dirname(__file__), '../schema')
    
    # 按顺序执行表、索引和视图的创建
    sql_files = [
        '../schema/tables/01_core_tables.sql',
        '../schema/tables/02_indexes.sql',
        '../schema/views/01_analysis_views.sql'
    ]
    
    for sql_file in sql_files:
        file_path = os.path.join(os.path.dirname(__file__), sql_file)
        with open(file_path, 'r') as f:
            cur.execute(f.read())
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_database()