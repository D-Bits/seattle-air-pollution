/* TODO: Write views for analysis */

CREATE VIEW vw_highest_aqi AS 
SELECT * 
FROM public.pollution 
ORDER BY aqi DESC;
