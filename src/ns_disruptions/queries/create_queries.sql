CREATE table ns_disruptions (
	id varchar(255),
	type varchar(255),
	impact int,
    fetch_timestamp TIMESTAMP
);

CREATE table ns_disruption_station_link (
    disruption_id varchar(255),
    station_code varchar(10),
    level varchar(255),
    fetch_timestamp TIMESTAMP -- in case code can be tied to multipe disruption ids
)

CREATE TABLE ns_stations (
	code varchar(10),
	name varchar(255),
	station_type varchar(255),
	location geometry
);