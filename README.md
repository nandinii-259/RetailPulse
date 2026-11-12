# RetailPulse – Retail Sales Data Engineering & Analytics Pipeline

An end-to-end data engineering project that processes retail sales data using Python, performs data cleaning and validation, stores structured data in SQLite, and generates business insights through SQL analytics and an interactive dashboard.

## Overview

RetailPulse simulates a real-world retail data processing system where sales records may contain duplicate transactions, missing values, invalid quantities, and incorrect prices.

The project implements an ETL pipeline to transform raw sales data into clean, structured, and analysis-ready information.

## Tech Stack

- **Programming:** Python
- **Data Processing:** Pandas
- **Database:** SQLite
- **Query Language:** SQL
- **Dashboard:** Streamlit
- **Visualization:** Plotly
- **Testing:** Python unittest
- **Version Control:** Git & GitHub

## Project Architecture

```text
RetailPulse/
│
├── data/
│   ├── raw/
│   │   └── sales.csv
│   └── processed/
│       ├── cleaned_sales.csv
│       ├── rejected_records.csv
│       └── transformed_sales.csv
│
├── src/
│   ├── validate.py
│   ├── transform.py
│   ├── load.py
│   └── analytics.py
│
├── tests/
│   └── test_pipeline.py
│
├── database/
├── logs/
│
├── main.py
├── dashboard.py
├── requirements.txt
└── .gitignore
```

## ETL Pipeline

The project follows three major ETL stages:

### 1. Extract
- Reads raw retail sales data from CSV files using Pandas.
- Performs initial data profiling.
- Identifies missing values and duplicate transactions.

### 2. Transform
- Validates transaction records.
- Detects duplicate transaction IDs.
- Identifies missing customer information and quantities.
- Rejects invalid quantities and negative prices.
- Calculates revenue using:

  `Revenue = Quantity × Unit Price`

- Saves cleaned, rejected, and transformed records separately.

### 3. Load
- Stores processed data in an SQLite database.
- Implements relational tables for customers, products, and sales.
- Uses primary keys and foreign key constraints.
- Implements UPSERT logic to insert new transactions and update existing records.

## Database Design

The SQLite database contains three tables:

| Table | Description |
|---|---|
| customers | Stores unique customer IDs |
| products | Stores unique product IDs |
| sales | Stores transaction details and calculated revenue |

The sales table maintains relationships with the customer and product tables using foreign keys.

## SQL Analytics

RetailPulse generates business insights through SQL queries:

- Total sales revenue
- Store-wise revenue analysis
- Product-wise revenue analysis
- Payment-method-wise revenue analysis

## Interactive Dashboard

Built using Streamlit and Plotly, the dashboard provides:

- Total Revenue KPI
- Total Transactions KPI
- Average Transaction Value KPI
- Store-wise revenue bar chart
- Product-wise revenue bar chart
- Payment-method distribution pie chart
- Interactive transaction table
- Store, product, and date filters

## Data Processing Results

The sample dataset contains 12 raw transactions.

| Metric | Result |
|---|---:|
| Total input records | 12 |
| Accepted records | 8 |
| Rejected records | 4 |
| Total Revenue | ₹2,16,700 |
| Average Transaction Value | ₹27,087.50 |

## Automated Testing

The project includes unit tests using Python's `unittest` framework.

Test cases cover:

- Duplicate transaction detection
- Revenue calculation
- Database primary key constraints
- UPSERT functionality

All 4 implemented test cases passed successfully.

## Installation & Execution

### 1. Clone the repository

```bash
git clone https://github.com/nandinii-259/RetailPulse.git
cd RetailPulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create required directories

```powershell
New-Item -ItemType Directory -Force database, logs
```

### 5. Run the ETL pipeline

```bash
python main.py
```

This extracts, validates, transforms, and loads the sales data into SQLite.

### 6. Launch the dashboard

```bash
python -m streamlit run dashboard.py
```

The dashboard will open in your browser at:

`http://localhost:8501`

### 7. Run unit tests

```bash
python -m unittest discover -s tests -v
```

## Future Enhancements

- Integrate Apache Spark and PySpark for large-scale data processing.
- Implement incremental data loading strategies.
- Integrate Databricks for cloud-based data engineering.
- Add automated pipeline scheduling and monitoring.
- Extend analytics with Power BI dashboards.

## Author

**Nandini Agrawal**

Electronics and Telecommunication Engineering

[GitHub](https://github.com/nandinii-259)

---

*RetailPulse demonstrates practical implementation of ETL workflows, data quality management, relational database design, SQL analytics, and interactive business intelligence.*