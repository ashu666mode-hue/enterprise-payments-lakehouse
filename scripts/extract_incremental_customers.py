import os
from datetime import datetime, timezone

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def get_watermark(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT watermark_timestamp
        FROM control.pipeline_watermarks
        WHERE pipeline_name = %s;
        """,
        ("customers_incremental",),
    )

    result = cursor.fetchone()
    cursor.close()

    return result[0]


def update_watermark(connection, new_watermark):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE control.pipeline_watermarks
        SET
            watermark_timestamp = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE pipeline_name = %s;
        """,
        (
            new_watermark,
            "customers_incremental",
        ),
    )

    connection.commit()
    cursor.close()


def extract_customers(watermark, high_watermark):
    connection = get_connection()

    query = """
        SELECT
            customer_id,
            first_name,
            last_name,
            date_of_birth,
            email,
            phone,
            customer_type,
            created_at,
            updated_at
        FROM customer.customers
        WHERE updated_at > %s
            AND updated_at <= %s
        ORDER BY updated_at;
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=[watermark, high_watermark],
    )

    connection.close()

    return dataframe


if __name__ == "__main__":
    connection = get_connection()
    watermark = get_watermark(connection)
    high_watermark = datetime.now(timezone.utc).replace(tzinfo=None)
    connection.close()

    df = extract_customers(watermark, high_watermark)

    print(f"Rows extracted: {len(df)}")

    if not df.empty:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = (
            f"data/bronze/customers/"
            f"customers_{timestamp}.csv"
        )

        df.to_csv(output_file, index=False)

        print(f"File written to: {output_file}")
    else:
        print("No changed customer records found.")

    connection = get_connection()
    update_watermark(connection, high_watermark)
    connection.close()