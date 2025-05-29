-- 0.0 affected station in the last 24 hours for the map
with disrupted_stations_24h as (
	select nd.id, ndsl.station_code, ndsl.level from ns.ns_disruptions nd
	join ns.ns_disruption_station_link ndsl on nd.id = ndsl.disruption_id
	where nd.fetch_timestamp >= now() - interval '24 hours'
	group by id, ndsl.station_code, ndsl.level
)
select * from disrupted_stations_24h ds
join ns.ns_stations st on ds.station_code = st.code


-- 1.0 per day aggregations (n active disruptions, % type disruptions, high/low/avg disruption_impact, % province?) --------
with day_disruptions as (
	select nd.id, nd.impact, nd.fetch_timestamp::date as day from ns.ns_disruptions nd group by day, nd.id, nd.impact
)
select dd.day, dd.id as disruption_id, dd.impact, ndsl.station_code, ndsl."level" from day_disruptions dd join ns.ns_disruption_station_link ndsl on dd.id = ndsl.disruption_id
group by dd.day, dd.id, ndsl.station_code, ndsl."level", dd.impact  -- for each day get the distinct disruption and its affected stations


-- 3.0 all time(last 30 days or group per month) : (total disruption, % type disruption, avg/high/low per disruptions per day, avg/high/low impact)

-- 4.0 per province


-- 1.1 per day aggregations - list stations per day -------------
with day_disruptions as (
	select nd.id, nd.fetch_timestamp::date as day from ns.ns_disruptions nd group by day, nd.id
)
select dd.day, dd.id, ndsl.station_code from day_disruptions dd join ns.ns_disruption_station_link ndsl on dd.id = ndsl.disruption_id 
group by dd.day, dd.id, ndsl.station_code 

--

-- map aggregations ()


SELECT column_name, udt_name
FROM information_schema.columns
WHERE table_name = 'ns_disruptions';
