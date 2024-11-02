import paho.mqtt.client as mqtt
from typing import Dict, Any, Callable
import json
import logging
from datetime import datetime

class LabMQTTClient:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = mqtt.Client()
        self.logger = logging.getLogger(__name__)
        self.handlers = {}
        
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.username_pw_set(
                self.config['username'],
                self.config['password']
            )
            self.client.connect(
                self.config['broker_host'],
                self.config['broker_port'],
                60
            )
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT broker: {str(e)}")
            raise
            
    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to a topic with handler"""
        self.handlers[topic] = handler
        self.client.subscribe(topic)
        self.logger.info(f"Subscribed to topic: {topic}")
        
    def publish(self, topic: str, payload: Dict[str, Any]):
        """Publish message to topic"""
        try:
            message = {
                'timestamp': datetime.utcnow().isoformat(),
                'data': payload
            }
            self.client.publish(topic, json.dumps(message))
            self.logger.debug(f"Published to {topic}: {payload}")
        except Exception as e:
            self.logger.error(f"Failed to publish message: {str(e)}")
            
    def on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects"""
        if rc == 0:
            self.logger.info("Connected to MQTT broker")
            # Resubscribe to topics
            for topic in self.handlers.keys():
                client.subscribe(topic)
        else:
            self.logger.error(f"Failed to connect to MQTT broker with code: {rc}")
            
    def on_message(self, client, userdata, msg):
        """Callback for when message is received"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            if topic in self.handlers:
                self.handlers[topic](payload)
            else:
                self.logger.warning(f"No handler for topic: {topic}")
                
        except json.JSONDecodeError:
            self.logger.error("Failed to decode message payload")
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            
    def on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects"""
        self.logger.warning(f"Disconnected from MQTT broker with code: {rc}")
        
    def start(self):
        """Start MQTT client loop"""
        self.client.loop_start()
        
    def stop(self):
        """Stop MQTT client loop"""
        self.client.loop_stop()
        self.client.disconnect()
