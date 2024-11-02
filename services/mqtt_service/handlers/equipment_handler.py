from typing import Dict, Any
from .base_handler import BaseHandler
from database.mongodb.connection import MongoDBConnection

class EquipmentHandler(BaseHandler):
    def __init__(self, db_connection: MongoDBConnection):
        self.db = db_connection
        
    def handle(self, payload: Dict[str, Any]):
        """Handle equipment data"""
        # Store raw data in MongoDB
        self.db.store_equipment_data(payload)
        
        # Process equipment-specific data
        if payload.get('type') == 'measurement':
            self._process_measurement(payload)
        elif payload.get('type') == 'status':
            self._process_status(payload)
            
    def _process_measurement(self, data: Dict[str, Any]):
        """Process measurement data"""
        # Extract measurements
        measurements = data.get('measurements', {})
        
        # Store processed data
        self.db.store_processed_measurement({
            'equipment_id': data['equipment_id'],
            'timestamp': data['timestamp'],
            'measurements': measurements,
            'metadata': data.get('metadata', {})
        })
        
    def _process_status(self, data: Dict[str, Any]):
        """Process equipment status"""
        # Update equipment status
        self.db.update_equipment_status(
            data['equipment_id'],
            data['status']
        )
