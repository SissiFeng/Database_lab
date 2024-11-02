from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

class GlueETLJob:
    def __init__(self):
        self.glue_context = GlueContext(SparkContext.getOrCreate())
        self.spark = self.glue_context.spark_session
        self.job = Job(self.glue_context)
    
    def process_experiment_data(self):
        # Read from source (e.g., S3)
        dynamic_frame = self.glue_context.create_dynamic_frame.from_catalog(
            database="lab_experiments",
            table_name="raw_experiments"
        )
        
        # Apply transformations
        mapped_frame = ApplyMapping.apply(
            frame=dynamic_frame,
            mappings=[
                ("experiment_id", "string", "experiment_id", "string"),
                ("timestamp", "timestamp", "timestamp", "timestamp"),
                ("parameters", "string", "parameters", "string"),
                ("results", "string", "results", "string")
            ]
        )
        
        # Write to destination (e.g., Snowflake)
        self.glue_context.write_dynamic_frame.from_options(
            frame=mapped_frame,
            connection_type="custom.snowflake",
            connection_options={
                "sfDatabase": "LAB_DB",
                "sfSchema": "PUBLIC",
                "sfWarehouse": "COMPUTE_WH"
            }
        )
