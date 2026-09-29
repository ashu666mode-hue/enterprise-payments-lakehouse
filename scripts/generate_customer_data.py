import os
import random

from faker import Faker
import psycopg2
from dotenv import load_dotenv


load_dotenv()

fake = Faker()


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def generate_customers(number_of_customers=1000):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        for _ in range(number_of_customers):
            first_name = fake.first_name()
            last_name = fake.last_name()
            date_of_birth = fake.date_of_birth(
                minimum_age=18,
                maximum_age=85
            )

            email = fake.unique.email()
            phone = fake.phone_number()[:30]

            customer_type = random.choice(
                ["INDIVIDUAL", "BUSINESS"]
            )

            cursor.execute(
                """
                INSERT INTO customer.customers
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    email,
                    phone,
                    customer_type
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING customer_id;
                """,
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    email,
                    phone,
                    customer_type,
                ),
            )

            customer_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO customer.customer_addresses
                (
                    customer_id,
                    address_type,
                    address_line_1,
                    city,
                    state,
                    postal_code,
                    country,
                    is_primary
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    customer_id,
                    "HOME",
                    fake.street_address(),
                    fake.city(),
                    fake.state(),
                    fake.postcode(),
                    "USA",
                    True,
                ),
            )

            cursor.execute(
                """
                INSERT INTO customer.customer_status_history
                (
                    customer_id,
                    status,
                    reason
                )
                VALUES (%s, %s, %s);
                """,
                (
                    customer_id,
                    "ACTIVE",
                    "Synthetic customer created",
                ),
            )

        connection.commit()

        print(
            f"Successfully generated "
            f"{number_of_customers} customers."
        )

    except Exception as error:
        connection.rollback()
        print(f"Error: {error}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_customers(1000)