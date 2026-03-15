# FinTracker ELT Pipeline


[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3776AB?style=flat&logo=python&logoColor=white)](https://www.sqlalchemy.org/) <!-- Using Python logo as SQLAlchemy doesn't have a dedicated simple icon -->
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A modern, containerized **ETL pipeline** that collects real-time commodity and cryptocurrency prices, applies the **Medallion Architecture** (Bronze → Silver → Gold), and prepares clean, analytics-ready data.

Data is pulled from the [Gold API](https://www.goldapi.io/) and stored in PostgreSQL with full auditability and idempotency. The data is pulled once in 15 minutes for demonstration. Time interval of the extraction can be customized in the airflow DAG.

## ✨ Features

- **Medallion Architecture** implementation  
  - Bronze: raw untouched data + batch UUID  
  - Silver: cleansed, typed, deduplicated source-of-truth  
  - Gold: fact & dimension tables optimized for BI / charting
- UUID-based **batch tracking** for traceability
- **Idempotent** loading (no duplicates even on re-runs)
- Docker + Docker Compose for one-command setup
- Persistent storage via volumes (history survives restarts)
- Supports: Gold, Silver, Bitcoin, Ethereum, Palladium, Copper, Platinum

## 🏗 Architecture Overview

The pipeline follows the **Medallion Architecture** pattern:

1. **Bronze** – Raw landing zone (as-received data + metadata)
2. **Silver** – Cleansed, validated, deduplicated core layer
3. **Gold**   – Business-friendly, denormalized tables for reporting & BI

```mermaid
graph TD
    A[Gold API<br>every ~15 min] -->|JSON price data| B[Extract<br>+ Generate UUID]
    B --> C[Save raw to CSV<br>landing_zone]
    C --> D[Bronze Table<br>raw + batch_id]
    D --> E[Archive CSV<br>by date]
    D --> F[Silver Transform<br>clean, cast types, deduplicate]
    F --> G[Silver Table<br>deduplicated source-of-truth]
    G --> H[Gold Layer<br>update facts & dimensions]
    H --> I[BI / Charting Tools<br>e.g. Metabase, Superset, Tableau]

```

 ### Pipeline Flow

```
EXTRACT PHASE           LOAD PHASE            TRANSFORM PHASE
─────────────           ──────────            ────────────────

┌─────────────┐
│ API Request │
│ Every 15min │
└──────┬──────┘
       │
       ▼
┌─────────────┐        ┌─────────────┐
│Generate UUID│        │  Read CSV   │
└──────┬──────┘        └──────┬──────┘
       │                      │
       ▼                      ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│Save to CSV  │───────▶│Add UUID if  │───────▶│Clean & Cast │
│landing_zone │        │ missing     │        │   Data      │
└─────────────┘        └──────┬──────┘        └──────┬──────┘
                              │                      │
                              ▼                      ▼
                       ┌─────────────┐        ┌─────────────┐
                       │Load to Bronze│        │Deduplicate  │
                       │   Table      │        │             │
                       └──────┬──────┘        └──────┬──────┘
                              │                      │
                              ▼                      ▼
                       ┌─────────────┐        ┌─────────────┐
                       │Archive File │        │Load to Silver│
                       │ by Date     │        │   Table     │
                       └─────────────┘        └──────┬──────┘
                                                      │
                                                      ▼
                                               ┌─────────────┐
                                               │Update Gold  │
                                               │   Layer     │
                                               └─────────────┘


```

## Tech Stack

- Python 3.11
 - Pandas 2.2.2, 
 - SQLAlchemy 2.0.43
- PostgreSQL 14+
- Docker 29.3.0 and Docker Compose v5.1.0
- Apache Airflow 3.0.0

## 🚀 Quick Start

### Prerequisites

For this pipeline to work properly, please make sure the following softwares are installed in the machine.

- Docker and Docker compose
- git

### 1. Compile the required custom images

This pipeline needs the images`cpd-python` and `airflow-with-dependencies` should be built before launching the pipeline. The `Dockerfile`s for these images are available in the root directory of the repository.


```bash
docker compose -t cpd-python . #this will use the `Dockerfile` to build the image.
docker compose -t airflow-with-dependencies -f Dockerfile-airflow .
```

### Launch the pipeline

Once the images are built,  the pipeline can be run using 

```bash
#Make sure you are in the project root directory

docker compose up -d # Remove the `-d` flag if you want to run the pipeline in interactive mode.
```

The pipeline will be launched and can be accessed using airflow UI at http://localhost:8080. You will need a password and this pipeline uses simple authentication manager. To see the password, you can use

```bash
docker exec -it commodity-price-tracker-airflow-manager-1 bash
```
Which will take you to the shell of the airflow-manager container. You can simply view the password stored in the file  `simple_auth_manager_passwords.json.generated` using a `cat` command.

```bash
cat /opt/airflow/simple_auth_manager_passwords.json.generated
```
Password is reset for every launch. In a future release, this will be upgraded to a production grade authentication system.

### Starting & Running the Pipeline

The pipeline is orchestrated with Apache Airflow and runs on a 15-minute schedule.

1. Open the Airflow web UI:  
   http://localhost:8080

2. Locate the main DAG  named `commodity-tracker-pipeline`.

3. **Manually trigger it once**:
   - Click the play/trigger icon next to the DAG.
   - This performs the initial run and verifies everything works.

4. After the first successful run, the DAG will **automatically execute every 15 minutes** (as configured in `schedule_interval`).

Each run:
- Pulls fresh commodity & crypto prices from the Gold API
- Processes data through the Medallion layers (Bronze → Silver → Gold)
- Stores results idempotently in the PostgreSQL database
- Archives raw files by date

No further manual steps are required.

### Accessing the Commodity Database

All processed price data (Bronze, Silver, Gold layers) is stored in a dedicated PostgreSQL database named **`commodity_db`**.

#### Connection (from inside Docker containers / Airflow tasks)

Airflow automatically creates a connection using this environment variable (already set in the `docker-compose.yml`):

```yaml
AIRFLOW_CONN_POSTGRES_DEFAULT: postgresql://myuser:secret@postgres:5432/commodity_db
```
This connection can be used inside container or be used in airflow DAG tasks.

#### Local connection

Here are the local connection details

- Host: localhost
- Port: 5433
- Database: commodity_db
- Username: myuser
- Password: secret

#### Security Note

These credentials (myuser / secret) are for local demo use only. In production, use strong passwords, secret management (Vault/AWS SSM), and never expose the database port publicly.