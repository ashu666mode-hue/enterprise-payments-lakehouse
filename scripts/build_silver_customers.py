import glob
import os

import pandas as pd


BRONZE_PATTERN = "data/bronze/customers/*.csv"
SILVER_OUTPUT = "data/silver/customers/customers_latest.csv"


def read_bronze_files():
    files = glob.glob(BRONZE_PATTERN)

    if not files:
        raise FileNotFoundError(
            "No Bronze customer files found."
        )

    dataframes = []

    for file_path in files:
        df = pd.read_csv(file_path)

        df["source_file"] = os.path.basename(file_path)

        dataframes.append(df)

    combined_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    return combined_df


def build_silver_customers(df):
    df["updated_at"] = pd.to_datetime(
        df["updated_at"]
    )

    df = df.sort_values(
        by=["customer_id", "updated_at"]
    )

    latest_df = df.drop_duplicates(
        subset=["customer_id"],
        keep="last"
    )

    latest_df = latest_df.sort_values(
        by="customer_id"
    )

    return latest_df


if __name__ == "__main__":
    bronze_df = read_bronze_files()

    print(
        f"Bronze rows read: {len(bronze_df)}"
    )

    silver_df = build_silver_customers(
        bronze_df
    )

    print(
        f"Silver rows after deduplication: "
        f"{len(silver_df)}"
    )

    os.makedirs(
        "data/silver/customers",
        exist_ok=True
    )

    silver_df.to_csv(
        SILVER_OUTPUT,
        index=False
    )

    print(
        f"Silver file written to: "
        f"{SILVER_OUTPUT}"
    )