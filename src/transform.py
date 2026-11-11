
import pandas as pd


def transform_sales(df):

    # Create a copy
    df = df.copy()

    # Convert order_date into datetime format
    df["order_date"] = pd.to_datetime(df["order_date"])

    # Calculate revenue
    df["revenue"] = df["quantity"] * df["unit_price"]

    print("\n--- TRANSFORMED SALES DATA ---")

    print(df.head())

    # Save transformed data
    df.to_csv("data/processed/transformed_sales.csv", index=False)

    print("\nTransformed sales data saved successfully!")



    return df
