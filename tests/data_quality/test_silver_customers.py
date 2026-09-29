import pandas as pd


SILVER_FILE = "data/silver/customers/customers_latest.csv"


def load_silver_customers():
    return pd.read_csv(SILVER_FILE)


def test_customer_id_is_unique():
    df = load_silver_customers()

    duplicate_count = df["customer_id"].duplicated().sum()

    assert duplicate_count == 0


def test_required_columns_are_not_null():
    df = load_silver_customers()

    required_columns = [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "customer_type",
    ]

    null_count = df[required_columns].isnull().sum().sum()

    assert null_count == 0


def test_customer_type_is_valid():
    df = load_silver_customers()

    allowed_values = {
        "INDIVIDUAL",
        "BUSINESS",
    }

    invalid_values = set(df["customer_type"]) - allowed_values

    assert invalid_values == set()


def test_email_is_unique():
    df = load_silver_customers()

    duplicate_email_count = df["email"].duplicated().sum()

    assert duplicate_email_count == 0