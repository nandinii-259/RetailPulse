import sqlite3



def create_connection():

    conn = sqlite3.connect("database/retailpulse.db")

    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")

    print("Database connection successful!")

    return conn



def create_tables(conn):

    cursor = conn.cursor()

    # Customers dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY
        )
    """)

    # Products dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY
        )
    """)

    # Sales fact table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id TEXT PRIMARY KEY,
            order_date TEXT,
            customer_id TEXT,
            product_id TEXT,
            store_id TEXT,
            quantity REAL,
            unit_price REAL,
            payment_method TEXT,
            revenue REAL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    conn.commit()

    print("Database tables created successfully!")


def load_dimensions(conn, df):

    cursor = conn.cursor()

    # Insert unique customer IDs
    customers = df["customer_id"].dropna().unique()

    for customer in customers:
        cursor.execute("""
            INSERT OR IGNORE INTO customers (customer_id)
            VALUES (?)
        """, (customer,))

    # Insert unique product IDs
    products = df["product_id"].dropna().unique()

    for product in products:
        cursor.execute("""
            INSERT OR IGNORE INTO products (product_id)
            VALUES (?)
        """, (product,))

    conn.commit()

    print("Customer and product tables populated successfully!")





def load_sales(conn, df):

    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute("""
            INSERT INTO sales (
                transaction_id,
                order_date,
                customer_id,
                product_id,
                store_id,
                quantity,
                unit_price,
                payment_method,
                revenue
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(transaction_id)
            DO UPDATE SET
                order_date = excluded.order_date,
                customer_id = excluded.customer_id,
                product_id = excluded.product_id,
                store_id = excluded.store_id,
                quantity = excluded.quantity,
                unit_price = excluded.unit_price,
                payment_method = excluded.payment_method,
                revenue = excluded.revenue
        """, (
            row["transaction_id"],
            str(row["order_date"]),
            row["customer_id"],
            row["product_id"],
            row["store_id"],
            row["quantity"],
            row["unit_price"],
            row["payment_method"],
            row["revenue"]
        ))

    conn.commit()

    print("Sales data loaded successfully using UPSERT!")



def verify_sales(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]

    print("\n--- DATABASE VERIFICATION ---")
    print("Total records in sales table:", count)
