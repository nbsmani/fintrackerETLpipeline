# FinTracker ETL Pipeline
A modern, containerized ETL pipeline designed to collect, transform, and warehouse commodity and crypto price data using the Medallion Architecture.

## 🚀 Overview
FinTracker automates the journey of financial data from raw API responses to analysis-ready database tables. It ensures data integrity through UUID-based batch tracking and prevents duplication using idempotent loading logic.

## 🏗 Architecture
The data flows through three distinct stages within a PostgreSQL database:

Bronze (Raw): The landing zone. Stores raw JSON/CSV data exactly as it arrived from the source, appended with a batch_id (UUID) for auditability.

Silver (Cleansed): The "Source of Truth." Data is cast to proper types (DECIMAL, TIMESTAMPTZ), deduplicated, and filtered for quality.

Gold (Analytics): The serving layer. Organized into Fact and Dimension tables optimized for high-speed BI and trend charting.

## 🛠 Tech Stack
Language: Python 3.x (Pandas, SQLAlchemy)

Database: PostgreSQL 14+

Infrastructure: Docker & Docker Compose

Data Format: CSV / JSON

🚦 Quick Start
1. Clone the repo and Configure:

```
git clone https://github.com/your-username/fintracker-etl.git
cd fintracker-etl
```

2. Launch the Environment:

```bash
docker-compose up -d
```
This will fetch the commodity prices for the following symbols
- XAG | Silver
- XAU | Gold
- BTC | Bitcoin
- ETH | Ethereum
- XPD | Palladium
- HG  | Copper
- XPT | Platinum

 from https://api.gold-api.com/price/{symbol} and ingest into a bronze table, cleaned and validated and inserted into a silver table, Then fact and dimension tables are generated in Gold layer, ready to serve to the analytics layer.


## 📈 Key Features
Batch Integrity: Uses uuid4 to "staple" records from the same instance together.

Idempotency: Silver promotion scripts use WHERE NOT EXISTS to ensure no data is double-counted.

Persistence: Docker volumes ensure your historical data survives container restarts.