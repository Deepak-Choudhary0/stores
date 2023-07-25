-- Table to store store status data
CREATE TABLE store_status (
    store_id VARCHAR(255) PRIMARY KEY,
    timestamp_utc TIMESTAMP NOT NULL,
    status VARCHAR(10) NOT NULL
);

-- Table to store business hours data
CREATE TABLE business_hours (
    store_id VARCHAR(255) PRIMARY KEY,
    day_of_week INTEGER NOT NULL,
    start_time_local TIME,
    end_time_local TIME
);

-- Table to store store timezones
CREATE TABLE store_timezones (
    store_id VARCHAR(255) PRIMARY KEY,
    timezone_str VARCHAR(255) NOT NULL
);

-- information about whether a report is "Running" or "Complete" based on its status.
CREATE TABLE report_status (
    report_id VARCHAR PRIMARY KEY,
    status VARCHAR NOT NULL
);