/* TODO: Write views for analysis */


-- Show pollution data by AQI
CREATE VIEW vw_highest_aqi AS 
SELECT * 
FROM public.pollution 
ORDER BY aqi DESC;

-- Show days with the most rainfall
CREATE VIEW vw_highest_rainfall AS 
SELECT * 
FROM public.atmospheric
ORDER BY precip_mm DESC;
