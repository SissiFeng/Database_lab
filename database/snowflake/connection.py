from snowflake.connector import connect
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

class SnowflakeConnection:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.engine = None
    
    def connect(self):
        self.connection = connect(
            user=self.config['user'],
            password=self.config['password'],
            account=self.config['account'],
            warehouse=self.config['warehouse'],
            database=self.config['database'],
            schema=self.config['schema']
        )
        
        self.engine = create_engine(URL(
            user=self.config['user'],
            password=self.config['password'],
            account=self.config['account'],
            warehouse=self.config['warehouse'],
            database=self.config['database'],
            schema=self.config['schema']
        ))
        
    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
