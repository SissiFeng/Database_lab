from pymongo import MongoClient
from typing import Dict, Any

class MongoDBConnection:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        self.db = None
    
    def connect(self):
        self.client = MongoClient(
            host=self.config['host'],
            port=self.config['port'],
            username=self.config['username'],
            password=self.config['password']
        )
        self.db = self.client[self.config['database']]
    
    def store_experiment_metadata(self, metadata: Dict[str, Any]):
        """Store experiment metadata in MongoDB"""
        collection = self.db.experiments
        return collection.insert_one(metadata)
    
    def store_unstructured_data(self, data: Dict[str, Any]):
        """Store unstructured experimental data"""
        collection = self.db.experiment_data
        return collection.insert_one(data)
    
    def find_experiments(self, query: Dict[str, Any]):
        """Query experiment metadata"""
        collection = self.db.experiments
        return collection.find(query)
