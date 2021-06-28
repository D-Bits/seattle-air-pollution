/* TODO: Write views for analysis */


-- Show pollution data by AQI
CREATE VIEW vw_highest_aqi AS 
SELECT last_updated, aqi 
FROM public.pollution 
ORDER BY aqi DESC;

-- Show days with the most rainfall
CREATE VIEW vw_highest_rainfall AS 
SELECT last_updated, precip_mm 
FROM public.atmospheric
ORDER BY precip_mm DESC;

-- Show hottest times
CREATE VIEW vw_hottest AS 
SELECT last_updated, temp_c
FROM public.atmospheric 
ORDER BY temp_c DESC;
