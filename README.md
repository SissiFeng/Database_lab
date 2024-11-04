# Laboratory Database Management System

A flexible and scalable database system designed for managing laboratory experiments and data processing workflows.

## Overview

This repository provides a comprehensive solution for:
- Experiment data collection and storage
- Data processing and transformation
- Quality control and monitoring
- Visualization and reporting

## Key Features

- **Data Management**
  - Robust database schema for experiment data
  - Version control and migrations
  - ETL/ELT pipelines for data integration

- **Data Processing**
  - Modular data processing framework
  - Customizable cleaning and transformation
  - Feature engineering capabilities

- **Workflow Management**
  - Automated workflows using Prefect
  - Data quality checks
  - Error handling and notifications

- **Visualization**
  - Real-time experiment monitoring
  - Interactive dashboards (Gradio)
  - Business intelligence integration (Tableau)

## Architecture

The system is built with modern data stack:
- PostgreSQL/Redshift for data storage
- dbt for data transformation
- Prefect for workflow orchestration
- Gradio/Tableau for visualization

## Project Structure

```
project-repo/
├── README.md
├── config/                         # Configuration files
│   ├── database.yml               # Database configuration
│   ├── tableau_config.yml         # Tableau integration config
│   ├── prefect_config.yml         # Workflow config
│   └── processing_config.yml      # Data processing config
├── data_processing/               # Data processing modules
│   ├── processors/                # Processing components
│   └── examples/                  # Usage examples
├── database/                      # Database related files
│   ├── migrations/                # Database version control
│   ├── schema/                    # Schema definitions
│   ├── postgresql/               # PostgreSQL implementation
│   ├── snowflake/                # Snowflake implementation
│   ├── mongodb/                  # MongoDB implementation
│   └── scripts/                  # Database scripts
├── dbt/                          # DBT transformations
│   ├── models/                   # Data models
│   ├── macros/                   # Custom macros
│   └── tests/                    # Data tests
├── etl/                         # ETL/ELT pipeline
│   ├── extractors/              # Data extraction
│   ├── transformers/            # Data transformation
│   ├── loaders/                 # Data loading
│   └── glue/                    # AWS Glue jobs
├── services/                    # Service components
│   ├── monitoring_service/      # Monitoring
│   └── mqtt_service/           # MQTT integration
├── utils/                      # Utility functions
├── visualization/              # Visualization components
│   ├── tableau/               # Tableau integration
│   └── gradio_dashboard/      # Gradio dashboards
└── workflows/                  # Workflow definitions
    ├── tasks/                 # Prefect tasks
    └── flows/                 # Prefect flows
```

### MQTT service structure

```
services/mqtt_service/
├── __init__.py
├── mqtt_client.py              # MQTT client implementation
├── handlers/                   # Message handlers
│   ├── __init__.py
│   ├── base_handler.py        # Base handler class
│   └── equipment_handler.py   # Equipment handlers
├── subscribers/               # Topic subscribers
│   ├── __init__.py
│   └── equipment_subscriber.py
└── config/                    # MQTT configuration
    └── mqtt_config.yml
```

### Database structure

```
database/
├── migrations/                # Database version control
├── schema/                   # Schema definitions
│   ├── tables/              # Table definitions
│   └── views/               # View definitions
├── postgresql/              # PostgreSQL specific
│   └── connection.py
├── snowflake/               # Snowflake specific
│   └── connection.py
├── mongodb/                 # MongoDB specific
│   └── connection.py
└── scripts/
    └── init_db.py          # Initialization
```

### ETL pipeline

```
etl/
├── config/
│   └── etl_config.yml        # ETL configuration
├── extractors/               # Data extraction modules
│   └── source_extractors/    # Source-specific extractors
├── transformers/             # Data transformation modules
├── loaders/                  # Data loading modules
│   ├── warehouse_loaders/    # Data warehouse specific loaders
│   └── database_loaders/     # Database specific loaders
└── glue/                     # AWS Glue implementations
    └── glue_job.py          # Glue job definitions
```

### DBT structure

```
dbt/
├── models/
│   ├── staging/             # Initial data models
│   ├── intermediate/        # Transformed models
│   └── marts/              # Business-specific models
├── macros/                 # Custom DBT macros
├── tests/                  # Custom DBT tests
├── dbt_project.yml        # DBT project config
└── profiles.yml           # Connection profiles
```

### Data processing

```
data_processing/
├── processors/
│   ├── __init__.py
│   ├── base_processor.py     # Base processor class
│   ├── cleaning_processor.py # Data cleaning processor
│   ├── transform_processor.py # Data transformation processor
│   └── feature_processor.py  # Feature engineering processor
└── examples/
    └── data_processing_example.py
```

### Workflows structure
```
workflows/
├── config/
│   └── prefect_config.yml    # Prefect configuration
├── tasks/                    # Prefect tasks
│   ├── data_quality.py
│   ├── extract_tasks.py
│   └── transform_tasks.py
└── flows/                    # Prefect flows
    └── data_pipeline.py
```


## Basic Usage Flow

### 1. **Database Setup**

```bash
# Initialize database schema
python database/scripts/init_db.py
```

### 2. **Data Processing**

Example of using the data processing pipeline:

```python
from data_processing.processors import DataProcessor, CleaningProcessor

# Initialize processor with configuration
processor = DataProcessor(config_path='config/processing_config.yml')
processed_data = processor.process(raw_data)
```

### 3. **Running Workflows**

Execute the data pipeline:

```python
from workflows.flows.data_pipeline import main_data_pipeline

# Run the pipeline
main_data_pipeline()
```

### 4. **Visualization**

Launch the monitoring dashboard:

```python
from visualization.gradio_dashboard.experiment_monitor import ExperimentMonitor

monitor = ExperimentMonitor()
monitor.launch()
```

---

## Common Use Cases

1. **Processing New Experiment Data**
   - Place raw data in the designated input location
   - Configure processing parameters
   - Run the data pipeline
   - View results in the dashboard

2. **Monitoring Experiments**
   - Access the Gradio dashboard for real-time monitoring
   - Check experiment status and metrics
   - Set up alerts for specific conditions

3. **Data Analysis**
   - Use dbt models for data transformation
   - Generate reports through Tableau
   - Export processed data for further analysis

---

## Configuration

Key configuration files:

- `config/database.yml` - Database connection settings
- `config/processing_config.yml` - Data processing parameters
- `config/prefect_config.yml` - Workflow settings

## Frontend Interface

The system includes a modern web interface built with React, providing an intuitive way to interact with the laboratory database system.

### Interface Features

1. **Dashboard Overview**
   - Real-time statistics of laboratory operations
   - Equipment status monitoring
   - Experiment progress tracking
   - Key performance indicators visualization

2. **Equipment Management**
   - Comprehensive equipment listing
   - Status tracking (Online, Offline, In Use, Maintenance)
   - Usage statistics and maintenance schedules
   - Equipment performance monitoring
   - Location tracking across laboratory rooms

3. **Experiment Management**
   - Experiment creation and tracking
   - Workflow design and execution
   - Real-time experiment status updates
   - Data collection and validation
   - Results visualization

4. **Data Analysis**
   - Interactive data visualization
   - Custom report generation
   - Data export capabilities
   - Trend analysis and insights

### Technical Stack

- **Frontend Framework**: React
- **UI Components**: Custom-designed components for laboratory management
- **State Management**: React Hooks
- **Routing**: React Router
- **Styling**: CSS Modules
- **Build Tool**: Vite

### Getting Started with Frontend

```bash
# Navigate to frontend directory
cd lab-manager-frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

The interface will be available at `http://localhost:5173` by default.