import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATABASE_PATH = Path(__file__).resolve().parent / "database" / "retailpulse.db"

st.set_page_config(
    page_title="RetailPulse | Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.25);
        padding: 1rem 1.1rem;
        border-radius: 0.7rem;
    }
    [data-testid="stMetric"] [data-testid="stMetricLabel"],
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("RetailPulse Sales Dashboard")
st.caption("Explore sales performance across stores, products, payment methods, and dates.")

if not DATABASE_PATH.is_file():
    st.error(
        f"Database not found at `{DATABASE_PATH}`. Make sure the ETL pipeline has "
        "created `database/retailpulse.db`."
    )
    st.stop()

connection = None

try:
    database_uri = f"{DATABASE_PATH.as_posix()}?mode=ro"
    connection = sqlite3.connect(f"file:{database_uri}", uri=True)

    date_bounds = pd.read_sql_query(
        "SELECT MIN(date(order_date)) AS min_date, "
        "MAX(date(order_date)) AS max_date FROM sales",
        connection,
    ).iloc[0]
    stores = pd.read_sql_query(
        "SELECT DISTINCT store_id FROM sales "
        "WHERE store_id IS NOT NULL ORDER BY store_id",
        connection,
    )["store_id"].tolist()
    products = pd.read_sql_query(
        "SELECT DISTINCT product_id FROM sales "
        "WHERE product_id IS NOT NULL ORDER BY product_id",
        connection,
    )["product_id"].tolist()

    start_default = (
        pd.to_datetime(date_bounds["min_date"]).date()
        if pd.notna(date_bounds["min_date"])
        else date.today()
    )
    end_default = (
        pd.to_datetime(date_bounds["max_date"]).date()
        if pd.notna(date_bounds["max_date"])
        else start_default
    )

    st.subheader("Filters")
    store_col, product_col, date_col = st.columns([1, 1, 2])
    with store_col:
        selected_store = st.selectbox("Store", ["All stores", *stores])
    with product_col:
        selected_product = st.selectbox("Product", ["All products", *products])
    with date_col:
        date_range = st.date_input(
            "Date range",
            value=(start_default, end_default),
            min_value=start_default,
            max_value=end_default,
            format="YYYY-MM-DD",
        )

    if isinstance(date_range, tuple):
        start_date = date_range[0] or start_default
        end_date = (
            date_range[1] or end_default
            if len(date_range) > 1
            else start_date
        )
    else:
        start_date = end_date = date_range

    conditions = ["date(order_date) BETWEEN ? AND ?"]
    parameters = [start_date.isoformat(), end_date.isoformat()]

    if selected_store != "All stores":
        conditions.append("store_id = ?")
        parameters.append(selected_store)
    if selected_product != "All products":
        conditions.append("product_id = ?")
        parameters.append(selected_product)
    where_clause = " AND ".join(conditions)

    kpis = pd.read_sql_query(
        f"""
        SELECT
            COALESCE(SUM(revenue), 0) AS total_revenue,
            COUNT(*) AS total_transactions,
            COALESCE(AVG(revenue), 0) AS average_transaction_value
        FROM sales
        WHERE {where_clause}
        """,
        connection,
        params=parameters,
    ).iloc[0]

    st.subheader("Performance overview")
    revenue_col, transactions_col, average_col = st.columns(3)
    revenue_col.metric("Total Revenue", f"₹{kpis['total_revenue']:,.2f}")
    transactions_col.metric("Total Transactions", f"{int(kpis['total_transactions']):,}")
    average_col.metric("Average Transaction Value", f"₹{kpis['average_transaction_value']:,.2f}")

    store_revenue = pd.read_sql_query(
        f"""
        SELECT store_id AS Store, SUM(revenue) AS Revenue
        FROM sales
        WHERE {where_clause}
        GROUP BY store_id
        ORDER BY Revenue DESC
        """,
        connection,
        params=parameters,
    )
    product_revenue = pd.read_sql_query(
        f"""
        SELECT product_id AS Product, SUM(revenue) AS Revenue
        FROM sales
        WHERE {where_clause}
        GROUP BY product_id
        ORDER BY Revenue DESC
        """,
        connection,
        params=parameters,
    )
    payment_revenue = pd.read_sql_query(
        f"""
        SELECT payment_method AS "Payment method", SUM(revenue) AS Revenue
        FROM sales
        WHERE {where_clause}
        GROUP BY payment_method
        ORDER BY Revenue DESC
        """,
        connection,
        params=parameters,
    )

    st.subheader("Revenue breakdown")
    store_col, product_col = st.columns(2)
    if not store_revenue.empty:
        store_chart = px.bar(
            store_revenue,
            x="Store",
            y="Revenue",
            title="Revenue by Store",
            color_discrete_sequence=["#2563eb"],
        )
        store_chart.update_layout(yaxis_title="Revenue (₹)", xaxis_title=None)
        store_col.plotly_chart(store_chart, use_container_width=True)
    else:
        store_col.info("No store revenue for the selected filters.")

    if not product_revenue.empty:
        product_chart = px.bar(
            product_revenue,
            x="Product",
            y="Revenue",
            title="Revenue by Product",
            color_discrete_sequence=["#0f766e"],
        )
        product_chart.update_layout(yaxis_title="Revenue (₹)", xaxis_title=None)
        product_col.plotly_chart(product_chart, use_container_width=True)
    else:
        product_col.info("No product revenue for the selected filters.")

    if not payment_revenue.empty:
        payment_chart = px.pie(
            payment_revenue,
            names="Payment method",
            values="Revenue",
            title="Revenue by Payment Method",
            hole=0.4,
        )
        st.plotly_chart(payment_chart, use_container_width=True)
    else:
        st.info("No payment-method revenue for the selected filters.")

    transactions = pd.read_sql_query(
        f"""
        SELECT
            transaction_id AS "Transaction ID",
            order_date AS "Order Date",
            customer_id AS "Customer ID",
            product_id AS "Product ID",
            store_id AS "Store ID",
            quantity AS Quantity,
            unit_price AS "Unit Price",
            payment_method AS "Payment Method",
            revenue AS Revenue
        FROM sales
        WHERE {where_clause}
        ORDER BY order_date DESC, transaction_id
        """,
        connection,
        params=parameters,
    )

    st.subheader("Sales transactions")
    st.dataframe(
        transactions,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Unit Price": st.column_config.NumberColumn(format="₹%.2f"),
            "Revenue": st.column_config.NumberColumn(format="₹%.2f"),
        },
    )
    st.caption(f"Showing {len(transactions):,} transactions matching the selected filters.")
except sqlite3.Error as error:
    st.error(f"Could not read the RetailPulse database: {error}")
finally:
    if connection is not None:
        connection.close()
