-- =====================================================
-- ENERGY MANAGEMENT SYSTEM (EMS)
-- DATABASE SCHEMA
-- =====================================================

-- =====================================================
-- USERS
-- =====================================================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- SITES
-- A user can manage multiple locations
-- =====================================================

CREATE TABLE sites (
    site_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    site_name VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- DEVICES
-- Smart Meter, Solar Panel, Battery, EV Charger, etc.
-- =====================================================

CREATE TABLE devices (
    device_id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    device_name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    manufacturer VARCHAR(100),
    installed_at DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ENERGY READINGS
-- Main time-series table
-- =====================================================

CREATE TABLE energy_readings (
    reading_id BIGSERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    reading_time TIMESTAMPTZ NOT NULL,
    power_kw NUMERIC(10,2) CHECK (power_kw >= 0),
    energy_kwh NUMERIC(10,2) CHECK (energy_kwh >= 0),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (device_id, reading_time)
);

-- =====================================================
-- SOLAR GENERATION
-- Tracks solar energy production per device
-- =====================================================

CREATE TABLE solar_generation (
    generation_id BIGSERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    generated_at TIMESTAMPTZ NOT NULL,
    generated_kwh NUMERIC(10,2) NOT NULL CHECK (generated_kwh >= 0),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- BATTERY STATUS
-- Tracks battery charge over time per device
-- =====================================================

CREATE TABLE battery_status (
    battery_status_id BIGSERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    recorded_at TIMESTAMPTZ NOT NULL,
    charge_percent NUMERIC(5,2) CHECK (charge_percent >= 0 AND charge_percent <= 100),
    charge_kwh NUMERIC(10,2) CHECK (charge_kwh >= 0),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ENERGY FORECASTS
-- ML model predictions
-- =====================================================

CREATE TABLE energy_forecasts (
    forecast_id BIGSERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    forecast_time TIMESTAMPTZ NOT NULL,
    predicted_kwh NUMERIC(10,2) NOT NULL CHECK (predicted_kwh >= 0),
    model_name VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ALERTS
-- Notifications and warnings
-- =====================================================

CREATE TABLE alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES sites(site_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'unread',
    acknowledged_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES
-- Important for time-series performance
-- =====================================================

CREATE INDEX idx_energy_readings_time
ON energy_readings(reading_time);

CREATE INDEX idx_energy_readings_device_time
ON energy_readings(device_id, reading_time);

CREATE INDEX idx_solar_generation_time
ON solar_generation(generated_at);

CREATE INDEX idx_battery_status_time
ON battery_status(recorded_at);

CREATE INDEX idx_energy_forecasts_time
ON energy_forecasts(forecast_time);

CREATE INDEX idx_alerts_site
ON alerts(site_id);
