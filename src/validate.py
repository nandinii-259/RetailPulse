
import pandas as pd


def validate_sales(df):

    # Create a copy of the original dataset
    df = df.copy()

    print("\n--- STARTING DATA VALIDATION ---")

    print("Total records received:", len(df))

    # Step 1: Convert quantity and unit_price into numeric values

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    print("\n--- AFTER DATA TYPE CONVERSION ---")

    print(df[["quantity", "unit_price"]].dtypes)
    # Step 2: Identify missing values

    print("\n--- MISSING VALUE CHECK ---")

    print("Missing quantities:", df["quantity"].isna().sum())

    print("Missing customer IDs:", df["customer_id"].isna().sum())

    # Step 3: Create rejection reason column

    df["rejection_reason"] = ""

    # Check missing quantity
    df.loc[
        df["quantity"].isna(),
        "rejection_reason"
    ] += "Missing quantity; "

    # Check missing customer ID
    df.loc[
        df["customer_id"].isna(),
        "rejection_reason"
    ] += "Missing customer ID; "

    # Step 4: Detect duplicate transactions

    duplicate_mask = df["transaction_id"].duplicated(keep="first")

    df.loc[
        duplicate_mask,
        "rejection_reason"
    ] += "Duplicate transaction ID; "

    # Step 5: Validate quantity

    df.loc[
        df["quantity"] <= 0,
        "rejection_reason"
    ] += "Invalid quantity; "


    # Step 6: Validate unit price

    df.loc[
        df["unit_price"] <= 0,
        "rejection_reason"
    ] += "Invalid unit price; "

    print("\n--- REJECTION REASONS ---")

    print(
        df.loc[
            df["rejection_reason"] != "",
            ["transaction_id", "rejection_reason"]
        ]
    )
    # Step 7: Separate accepted and rejected records

    accepted_df = df[df["rejection_reason"] == ""].copy()

    rejected_df = df[df["rejection_reason"] != ""].copy()

    # Display record counts

    print("\n--- DATA QUALITY REPORT ---")

    print("Total records:", len(df))
    print("Accepted records:", len(accepted_df))
    print("Rejected records:", len(rejected_df))

    # Step 8: Save processed records

    accepted_df = accepted_df.drop(columns=["rejection_reason"])

    accepted_df.to_csv(
        "data/processed/cleaned_sales.csv",
        index=False
    )

    rejected_df.to_csv(
        "data/processed/rejected_records.csv",
        index=False
    )

    print("\nProcessed CSV files saved successfully!")

    return accepted_df, rejected_df
