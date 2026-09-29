CREATE TABLE IF NOT EXISTS customer.customers
(
    customer_id BIGSERIAL PRIMARY KEY,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,

    date_of_birth DATE NOT NULL,

    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30),

    customer_type VARCHAR(20) NOT NULL
        CHECK (customer_type IN ('INDIVIDUAL', 'BUSINESS')),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS customer.customer_addresses
(
    address_id BIGSERIAL PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    address_type VARCHAR(20) NOT NULL
        CHECK (address_type IN ('HOME', 'MAILING', 'BUSINESS')),

    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),

    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'USA',

    is_primary BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_address_customer
        FOREIGN KEY (customer_id)
        REFERENCES customer.customers(customer_id)
);


CREATE TABLE IF NOT EXISTS customer.customer_status_history
(
    status_history_id BIGSERIAL PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    status VARCHAR(20) NOT NULL
        CHECK (status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'CLOSED')),

    effective_from TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    effective_to TIMESTAMP,

    reason VARCHAR(255),

    CONSTRAINT fk_status_customer
        FOREIGN KEY (customer_id)
        REFERENCES customer.customers(customer_id),

    CONSTRAINT chk_status_dates
        CHECK (
            effective_to IS NULL
            OR effective_to >= effective_from
        )
);