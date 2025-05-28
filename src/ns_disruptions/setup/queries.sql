CREATE TABLE coins_data (
    name VARCHAR(255),
    price DECIMAL(18, 8),
    change_24h DECIMAL(20, 2),
    volume_24h DECIMAL(20, 2),
    market_cap DECIMAL(20, 2),
    fetch_timestamp DATETIME
);

CREATE table ns_disruptions (
	id varchar(255),
	type varchar(255),
	impact int,
    fetch_timestamp TIMESTAMP
);

CREATE table ns_disruption_station_link (
    disruption_id varchar(255),
    station_code varchar(10),
    fetch_timestamp TIMESTAMP -- in case code can be tied to multipe disruption ids
)

CREATE TABLE ns_stations (
	name varchar(255),
	code varchar(10),
	location geometry
);