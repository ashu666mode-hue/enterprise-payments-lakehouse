CREATE SCHEMA IF NOT EXISTS control;

CREATE TABLE IF NOT EXISTS control.pipeline_watermarks
(
    pipeline_name VARCHAR(100) PRIMARY KEY,
    watermark_timestamp TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);