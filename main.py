
import pandas as pd
import logging

from src.validate import validate_sales
from src.transform import transform_sales

from src.load import (
    create_connection,
    create_tables,
    load_dimensions,
    load_sales,
    verify_sales
)

from src.analytics import (
    get_total_revenue,
    get_store_revenue,
    get_product_revenue,
    get_payment_revenue
)


# Logging configuration
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Start pipeline
logger.info("RetailPulse ETL pipeline started")


# Step 1: Extract data
df = pd.read_csv("data/raw/sales.csv")

logger.info(f"Extracted {len(df)} records from sales.csv")


# Step 2: Display raw dataset
print("\n--- SALES DATA ---")
print(df)


# Step 3: Display first five records
print("\n--- FIRST FIVE RECORDS ---")
print(df.head())


# Step 4: Display dataset dimensions
print("\n--- DATASET SHAPE ---")
print(df.shape)


# Step 5: Display column information
print("\n--- DATASET INFORMATION ---")
df.info()


# Step 6: Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())


# Step 7: Check duplicate transactions
print("\n--- DUPLICATE TRANSACTIONS ---")
print(df["transaction_id"].duplicated().sum())


# Step 8: Validate sales data
cleaned_df, rejected_df = validate_sales(df)

logger.info(
    f"Validation completed: {len(cleaned_df)} accepted, "
    f"{len(rejected_df)} rejected"
)


# Step 9: Transform accepted sales data
transformed_df = transform_sales(cleaned_df)

logger.info("Sales data transformation completed")


# Step 10: Database operations
conn = create_connection()

try:

    # Create database tables
    create_tables(conn)

    # Load dimension tables first
    load_dimensions(conn, transformed_df)

    # Load sales fact table
    load_sales(conn, transformed_df)

    logger.info(
        f"Loaded {len(transformed_df)} sales records into SQLite"
    )

    # Verify database records
    verify_sales(conn)

    # Step 11: SQL Analytics

    get_total_revenue(conn)

    get_store_revenue(conn)

    get_product_revenue(conn)

    get_payment_revenue(conn)

    logger.info("RetailPulse ETL pipeline completed successfully")

except Exception:

    logger.exception("An error occurred during database processing")

    raise

finally:

    # Always close database connection
    conn.close()

    logger.info("Database connection closed")
