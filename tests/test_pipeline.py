
import unittest
import pandas as pd
import sqlite3

from src.validate import validate_sales
from src.transform import transform_sales
from src.load import create_tables, load_dimensions, load_sales


class TestRetailPulse(unittest.TestCase):

    def setUp(self):
        # Create sample sales data
        self.df = pd.DataFrame({
            "transaction_id": ["T101", "T102", "T102", "T103"],
            "order_date": [
                "2026-11-01",
                "2026-11-01",
                "2026-11-01",
                "2026-11-02"
            ],
            "customer_id": ["C001", "C002", "C002", "C003"],
            "product_id": ["P001", "P002", "P002", "P003"],
            "store_id": ["S01", "S01", "S01", "S02"],
            "quantity": [2, 5, 5, 3],
            "unit_price": [500, 100, 100, 200],
            "payment_method": ["UPI", "Cash", "Cash", "Card"]
        })

    def test_duplicate_detection(self):
        cleaned, rejected = validate_sales(self.df)

        self.assertEqual(len(cleaned), 3)
        self.assertEqual(len(rejected), 1)

    def test_revenue_calculation(self):
        sample = self.df.iloc[[0]].copy()

        transformed = transform_sales(sample)

        self.assertEqual(transformed.iloc[0]["revenue"], 1000)

    def test_database_primary_key(self):
        conn = sqlite3.connect(":memory:")

        try:
            conn.execute("""
                CREATE TABLE sales (
                    transaction_id TEXT PRIMARY KEY
                )
            """)

            conn.execute(
                "INSERT INTO sales VALUES (?)",
                ("T101",)
            )

            conn.execute(
                "INSERT OR IGNORE INTO sales VALUES (?)",
                ("T101",)
            )

            count = conn.execute(
                "SELECT COUNT(*) FROM sales"
            ).fetchone()[0]

            self.assertEqual(count, 1)

        finally:
            conn.close()

    def test_upsert_updates_existing_transaction(self):

        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON")

        try:
            create_tables(conn)

            # Original transaction
            original = pd.DataFrame({
                "transaction_id": ["T101"],
                "order_date": ["2026-11-01"],
                "customer_id": ["C001"],
                "product_id": ["P001"],
                "store_id": ["S01"],
                "quantity": [2],
                "unit_price": [500],
                "payment_method": ["UPI"],
                "revenue": [1000]
            })

            load_dimensions(conn, original)
            load_sales(conn, original)

            # Updated transaction
            updated = original.copy()
            updated.loc[0, "quantity"] = 3
            updated.loc[0, "revenue"] = 1500

            load_sales(conn, updated)

            cursor = conn.cursor()

            cursor.execute("""
                SELECT quantity, revenue
                FROM sales
                WHERE transaction_id = 'T101'
            """)

            result = cursor.fetchone()

            self.assertEqual(result, (3.0, 1500.0))

            # Verify no duplicate transaction was created
            cursor.execute("SELECT COUNT(*) FROM sales")

            self.assertEqual(cursor.fetchone()[0], 1)

        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
