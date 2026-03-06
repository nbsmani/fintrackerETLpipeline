# FinTracker ETL Pipeline

<div align="center">
  
  ![Python](https://img.shields.io/badge/Python-3.11-blue)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue)
  ![Apache Airflow](https://img.shields.io/badge/Airflow-2.7-green)
  ![Docker](https://img.shields.io/badge/Docker-24.0-blue)
  ![License](https://img.shields.io/badge/License-MIT-yellow)
  
  **Automated ETL Pipeline for Real-Time Commodity and Cryptocurrency Price Data**
  
  [Features](#-features) • 
  [Architecture](#-architecture) • 
  [Quick Start](#-quick-start) • 
  [Documentation](#-documentation) • 
  [Contributing](#-contributing)
  
</div>

---

## 📋 Overview

FinTracker is a production-ready ETL pipeline that automates the collection, transformation, and warehousing of financial market data. Built on the **Medallion Architecture**, it ensures data quality, auditability, and analytical readiness from raw API responses to curated business insights.

### Why FinTracker?

- **Real-time Data**: Fetches prices every 15 minutes for 7+ commodities/cryptocurrencies
- **Data Integrity**: UUID-based batch tracking prevents duplication
- **Scalable Design**: Medallion architecture enables easy extension
- **Containerized**: Run anywhere with Docker
- **Production Ready**: Airflow orchestration with error handling

---

## 🎯 Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Automated Ingestion** | Fetches real-time prices from [gold-api.com](https://gold-api.com) |
| **Multi-Asset Support** | Gold (XAU), Silver (XAG), Bitcoin (BTC), Ethereum (ETH), and more |
| **Data Lineage** | Every record tagged with UUID batch_id for complete traceability |
| **Idempotent Loading** | Duplicate prevention using batch_id tracking |
| **Incremental Processing** | Only new data promoted to silver layer |
| **Automated Archiving** | Processed files organized by date in archive directory |

### Supported Symbols

| Symbol | Asset | Type |
|--------|-------|------|
| XAU | Gold | Commodity |
| XAG | Silver | Commodity |
| XPT | Platinum | Commodity |
| XPD | Palladium | Commodity |
| HG | Copper | Commodity |
| BTC | Bitcoin | Cryptocurrency |
| ETH | Ethereum | Cryptocurrency |

---

## 🏗 Architecture

### Medallion Data Layers

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │              │     │             │     │             │
│  Gold-API   │────▶│ Landing Zone │────▶│ Bronze Layer│────▶│ Silver Layer│
│             │     │  CSV Files   │     │  Raw Data   │     │ Cleansed Data│
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
                                                                     │
                                                               ┌─────▼─────┐
                                                               │Gold Layer │
                                                               │Analytics  │
                                                               └───────────┘
```

### Layer Details

#### 🥉 Bronze Layer (Raw)

- **Purpose**: Immutable landing zone for raw API responses
- **Storage**: Raw JSON/CSV data with original structure
- **Audit**: Each batch tagged with unique UUID
- **Table**: `bronze.bronze_prices`

#### 🥈 Silver Layer (Cleansed)

- **Purpose**: Single source of truth with cleaned data
- **Transformations**: 
  - Data type casting (DECIMAL, TIMESTAMPTZ)
  - Deduplication via batch_id
  - Null value filtering
- **Table**: `silver.silver_prices`

#### 🥇 Gold Layer (Analytics)

- **Purpose**: Business-ready dimensional model
- **Structure**: Fact and dimension tables
- **Optimized for**: BI tools and trend analysis
- **Tables**: 
  - `gold.dim_commodity`
  - `gold.fact_prices`

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

---

## 🛠 Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | Apache Airflow 2.7 | Workflow scheduling & monitoring |
| **Database** | PostgreSQL 14 | Data warehousing |
| **Processing** | Python 3.11 | ETL logic |
| **Containerization** | Docker 24.0 | Environment isolation |
| **Data Processing** | Pandas 2.2 | Data transformation |
| **API Integration** | Requests 2.32 | External API calls |

### Key Libraries

```txt
pandas==2.2.2        # Data manipulation
SQLAlchemy==2.0.43   # Database connectivity
psycopg2-binary==2.9.11 # PostgreSQL adapter
requests==2.32.5     # API requests
apache-airflow==2.7.0 # Workflow orchestration
```

---

## 🚀 Quick Start

### Prerequisites

- Docker 24.0+ and Docker Compose 2.20+
- Python 3.11+ (for local development)
- 4GB RAM minimum
- 10GB free disk space

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/fintracker-etl.git
   cd fintracker-etl
   ```

2. **Build Docker images**

   Create a `build.sh` file:

   ```bash
   #!/bin/bash
   echo "Building Docker images..."
   docker build -t cpd-extractor -f Dockerfile_extractor.txt .
   docker build -t cpd-loader -f Dockerfile_loader.txt .
   docker build -t airflow-with-docker:latest -f Dockerfile_airflow.txt .
   echo "Build complete!"
   ```

   Make it executable and run:

   ```bash
   chmod +x build.sh
   ./build.sh
   ```

3. **Launch the environment**

   ```bash
   docker-compose up -d
   ```

4. **Verify installation**

   ```bash
   # Check container status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

5. **Access services**

   | Service | URL | Credentials |
   |---------|-----|-------------|
   | Airflow UI | http://localhost:8080 | airflow / airflow |
   | PostgreSQL (main) | localhost:5432 | myuser / secret / commodity_db |
   | PostgreSQL (Airflow) | localhost:5433 | airflow_user / secret / airflow_metadata |

---

## 📊 Usage Guide

### Running the Pipeline

The pipeline runs automatically every 15 minutes via Airflow. To trigger manually:

1. **Access Airflow UI**

   ```bash
   open http://localhost:8080
   ```

2. **Trigger DAG**

   - Navigate to DAGs → `commodity-tracker-pipeline`
   - Click the "Play" button → "Trigger DAG"

3. **Monitor execution**

   - View task logs for `extract_commodity_prices` and `load_commodity_prices_to_bronze`
   - Check tree view for task status

### Database Exploration

Connect to PostgreSQL and explore the data:

```bash
# Connect to main database
docker exec -it commodity-price-tracker_postgres_1 psql -U myuser -d commodity_db
```

**Sample Queries:**

```sql
-- Check bronze layer
SELECT COUNT(*), MIN(ingested_at), MAX(ingested_at) 
FROM bronze.bronze_prices;

-- Check silver layer with deduplication
SELECT commodity_name, COUNT(*) as records, 
       MIN(api_updated_at) as oldest_price
FROM silver.silver_prices
GROUP BY commodity_name;

-- Join across layers
SELECT 
    b.name,
    b.price as raw_price,
    s.price as cleaned_price,
    b.updatedat as api_time
FROM bronze.bronze_prices b
JOIN silver.silver_prices s ON b.uuid = s.batch_id
LIMIT 10;
```

### Data Directory Structure

```
data/
├── landing_zone/          # Incoming CSV files
│   └── priceYYYY-MM-DD-HH-MM-SS.csv
├── archive/               # Processed files
│   └── YYYY/
│       └── MM/
│           └── DD/
│               └── priceYYYY-MM-DD-HH-MM-SS.csv
└── symbols.csv            # Cached symbols list
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file for custom configuration:

```env
# Database credentials
POSTGRES_USER=myuser
POSTGRES_PASSWORD=secret
POSTGRES_DB=commodity_db

# Airflow metadata DB
AIRFLOW_USER=airflow_user
AIRFLOW_PASSWORD=secret

# Pipeline settings
FETCH_INTERVAL_MINUTES=15
API_BASE_URL=https://api.gold-api.com
```

### Docker Compose Overrides

For production deployment, create `docker-compose.override.yml`:

```yaml
version: '3.8'
services:
  postgres:
    restart: always
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  
  airflow-manager:
    environment:
      AIRFLOW__CORE__FERNET_KEY: ${FERNET_KEY}
      AIRFLOW__WEBSERVER__SECRET_KEY: ${SECRET_KEY}
```

---

## 📈 Monitoring & Maintenance

### Health Checks

```bash
# Check all services
docker-compose ps

# View real-time logs
docker-compose logs -f airflow-manager

# Database health
docker exec -it commodity-price-tracker_postgres_1 pg_isready -U myuser
```

### Backup & Recovery

```bash
# Backup database
docker exec -t commodity-price-tracker_postgres_1 pg_dump -U myuser commodity_db > backup.sql

# Restore database
cat backup.sql | docker exec -i commodity-price-tracker_postgres_1 psql -U myuser -d commodity_db
```

### Common Tasks

**Clear all data and restart:**

```bash
docker-compose down -v
docker-compose up -d
```

**Update symbols list:**

```bash
# Symbols auto-fetch on first run
# To force refresh, delete the cached file
rm data/symbols.csv
docker-compose restart extractor
```

---

## 🧪 Testing

### Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v --cov=./
```

### Integration Tests

```bash
# Test database connection
python scripts/test_connection.py

# Test API connectivity
python scripts/test_api.py
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run linters
flake8 scripts/
black scripts/
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Port conflicts** | Change ports in docker-compose.yml |
| **Permission denied** | `chmod -R 777 data/` |
| **Airflow can't connect to Docker** | Ensure docker.sock permissions: `sudo chmod 666 /var/run/docker.sock` |
| **Database connection refused** | Wait for healthcheck to pass |
| **No data in bronze layer** | Check API availability: `curl https://api.gold-api.com/price/XAU` |

### Debug Mode

Enable verbose logging in `docker-compose.yml`:

```yaml
environment:
  - AIRFLOW__LOGGING__LEVEL=DEBUG
```

---

## 📚 API Reference

### Gold-API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/symbols` | GET | List all available symbols |
| `/price/{symbol}` | GET | Get current price for symbol |

Rate Limits: Unlimited free access for development

---

## 🔮 Roadmap

- [x] Bronze layer implementation
- [x] Silver layer with deduplication
- [ ] Gold layer dimensional model
- [ ] Data quality metrics dashboard
- [ ] Alerting for price anomalies
- [ ] Historical backfill capability
- [ ] Support for additional data sources
- [ ] Real-time streaming option (Kafka)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👥 Authors

- **Balasubramaniam Namasivayam** - *Initial work* - [GitHub](https://github.com/your-username)

---

## 🙏 Acknowledgments

- [Gold-API](https://gold-api.com) for providing free financial data
- Apache Airflow community
- PostgreSQL team

---

<div align="center">
  
  **⭐ If you find this project useful, please consider giving it a star! ⭐**
  
  [Report Bug](https://github.com/your-username/fintracker-etl/issues) · 
  [Request Feature](https://github.com/your-username/fintracker-etl/issues) · 
  [Documentation](https://github.com/your-username/fintracker-etl/wiki)
  
</div>