
CREATE TABLE pollution
(
    id SERIAL PRIMARY KEY,
    dates TIMESTAMP NOT NULL,
    -- Air quality index
    aqi DECIMAL NOT NULL,
    co DECIMAL NOT NULL,
    "no" DECIMAL NOT NULL,
    no2 DECIMAL NOT NULL,
    o3 DECIMAL NOT NULL,
    pm2_5 DECIMAL NOT NULL,
    pm10 DECIMAL NOT NULL,
    so2 DECIMAL NOT NULL,
    -- Ammonia
    nh3 DECIMAL NOT NULL
);

CREATE TABLE solar_radiation
(
    id SERIAL PRIMARY KEY,
    dates TIMESTAMP NOT NULL,
    ghi DECIMAL NOT NULL,
    dni DECIMAL NOT NULL,
    dhi DECIMAL NOT NULL,
    ghi_cs DECIMAL NOT NULL,
    dni_cs DECIMAL NOT NULL,
    dhi_cs DECIMAL NOT NULL
);