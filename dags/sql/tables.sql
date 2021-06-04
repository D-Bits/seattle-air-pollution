
CREATE TABLE pollution
(
    id SERIAL PRIMARY KEY,
    dates TIMESTAMP NOT NULL,
    -- Air quality index
    aqi DECIMAL NOT NULL,
    co DECIMAL NOT NULL,
    "no" DECIMAL NOT NULL,
    no2 DECIMAL NOT NULL,
    -- Ozone
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
    -- cloudy global horizontal irradiance
    ghi DECIMAL NOT NULL,
    -- cloudy direct normal irradiance
    dni DECIMAL NOT NULL,
    -- cloudy diffuse horizontal irradiance
    dhi DECIMAL NOT NULL,
    -- clear sky irradiance values
    ghi_cs DECIMAL NOT NULL,
    dni_cs DECIMAL NOT NULL,
    dhi_cs DECIMAL NOT NULL
);