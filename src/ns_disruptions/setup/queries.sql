CREATE TABLE coins_data (
    name VARCHAR(255),
    price DECIMAL(18, 8),
    change_24h DECIMAL(20, 2),
    volume_24h DECIMAL(20, 2),
    market_cap DECIMAL(20, 2),
    fetch_timestamp DATETIME
);

CREATE table ns_train_disruptions (
	id varchar(255),
	coordinates geometry,
	niveau varchar(255),
	disruption_type varchar(255),
    fetch_timestamp TIMESTAMP
);

CREATE table ns_station_disruptions (
    id varchar(255),
    code varchar(10),
    fetch_timestamp TIMESTAMP -- in case code can be tied to multipe disruption ids
)

CREATE TABLE ns_stations (
	name varchar(255),
	code varchar(10),
	location geometry
);