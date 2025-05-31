-- 0.0: last 24 hours affected stations : grouped on date level
CREATE MATERIALIZED VIEW ns.disruptions_24h AS
WITH disrupted_stations_24h AS (
	SELECT nd.fetch_timestamp::date AS fetch_date, nd.id, ndsl.station_code, ndsl.LEVEL
	FROM ns.ns_disruptions nd
	JOIN ns.ns_disruption_station_link ndsl ON nd.id = ndsl.disruption_id
	WHERE nd.fetch_timestamp >= now() - interval '24 hours'
	GROUP BY nd.id, nd.fetch_timestamp::date, ndsl.station_code, ndsl.level
)
SELECT * FROM disrupted_stations_24h ds
JOIN ns.ns_stations nst ON ds.station_code = nst.code -- this join removes non-NL stations, so only NL stations included


-- 1.5 map data for displaying all the affected stations of the last 24h, grouped on station, counting disruption for each station
CREATE MATERIALIZED VIEW ns.map_data AS
SELECT
	station_code, count(id) AS involved_disruptions, "level", "name", station_type, "location"
FROM (
	SELECT DISTINCT ON (id, station_code) *
	FROM ns.disruptions_24h
) AS disruptions_stations -- deduplicate pairs from different dates, just pick the first as it wont differ
GROUP BY station_code, "level", "name", station_type, location


-- 2.0 per day aggregations, for last 30 days -----------
CREATE MATERIALIZED view ns.day_aggregations AS
WITH day_disruptions AS (
	SELECT nd.fetch_timestamp::date AS day, nd.id, nd.type, nd.impact FROM ns.ns_disruptions nd
	GROUP BY day, nd.id, nd.impact, nd.type
)
SELECT 
	dd.day,
	dd.type,
	count(dd.id),
	round(avg(dd.impact), 2) as avg_impact,
	round(max(dd.impact), 2) as max_impact,
	round(min(dd.impact), 2) as min_impact,
	round(count(*) / sum(count(*)) OVER (PARTITION BY dd.day), 2) * 100 AS perc
FROM day_disruptions dd
GROUP BY dd."day", dd."type"


-- 3.0 all time(last 30 days or group per month) : (total disruption, % type disruption, avg/high/low per disruptions per day, avg/high/low impact)
-- e4.0 per province?
-- e5.0 stations based?
