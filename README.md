# Anonymization Tool

V0.7


## General definitions

### Expected Travels Format

![Travel Data Format](https://github.com/travelai-public/anonymization-tool/blob/main/docs/travelai-overview.png)

The anonymization tool expect travels data in specific format, using five different travel object definitions:

#### Segments
Segments are roughly daily, unbroken series of travel data.

#### Routes
Route is defined as a single transportation period taken in order to transit between origin and destination, i.e., between Places A and B. Typical example Routes include transporting from home to work, or from work to lunch place. Route consists of one or more GISLegs.

#### GISLegs
GISLeg is defined as a transportation period with a single transportation mode. If one was talking in terms of transport or network graphs, a leg would be an edge, while stops or stations in graph theory are called nodes. Example GISLegs include bus or train journey, walking from office to station or cycling from home to office. The GIS prefix notes that the leg has been matched to transportation network.

#### Waypoints
Waypoint is a geolocation container that can include additional details such as transportation mode, time, accuracy, and velocity.

#### Places
Place is defined as a location where a user spends significant amounts of time, and often includes a meaningful real-world correspondence. Example Places include user-specific locations such as home and office, or public areas such as shopping malls and parks. 

### Database Format

The software expects the following structure for the input database:

#### public.segments
- id integer,  
- installation_id text,  
- start_ts bigint,  
- end_ts bigint,  
- routes_count integer,  
- legs_count integer,  
- gaps_count integer,  
- start_place_id integer,  
- end_place_id integer,  
- gislegs_count integer  

#### public.routes
- id integer,  
- installation_id text,  
- start_ts bigint,  
- end_ts bigint,  
- distance real,
- gis_distance real,
- duration integer,
- start_place integer,
- end_place integer,
- start_dwell integer,
- end_dwell integer,
- data_quality text,
- match_confidence real,
- segment_id integer


#### public.gis_legs
- id integer,  
- installation_id text,  
- start_ts bigint,  
- end_ts bigint,  
- transport_mode integer,
- distance real,
- duration real,
- match_confidence real,
- route_id integer,
- first_location geometry,
- last_location geometry


#### public.waypoints
- installation_id text,
- route_id integer,
- gisleg_id integer,
- timestamp bigint,
- transport_mode integer,
- location geometry,
- accuracy real,
- vaccuracy real,
- speed real,
- provider integer


#### public.places
- timestamp bigint,
- id integer,
- installation_id text,
- location geometry,
- dwelltime_sum real,
- dwelltime_percentage real,
- dwelltime_rank integer,
- label text,
- placeloc_strength real,
- first_dwell_starttime bigint,
- last_dwell_endtime bigint,
- place_reverse_goecode_id bigint

## Installation Instructions

Using PIP environment, the anonymization tool will automatically install and setup all the necessary dependencies. 

Be sure to set and export the variables in your virtual environemnt. 

### Database Settings

The software will automatically load the settings and connect to the DB according to the following environment variables:

	DB_USERNAME
	DB_HOST
	DB_PORT
	DB_NAME

The anonymization tool will automatically revert to development configuration if no such settings can be found in the enviroment. 

### Anonymization Settings

The anonymization setting can be exported in the following environment variables.

	K_ANON
	SUPPRESION

The anonymization tool will automatically load the settings avaibale at the "settings" file if no seetings can be found in the enviroment.


## Usage

The argument **installation_id** is optional. 
In cases you wish to anonymize individual records based on the installation_id, be sure to provide that identifier upon startup. 
When no **installation_id** is provided, the software will automatically assume a global dataset anonymization mechanism.

To run the tool go to **/src** directory and execute:

    pipenv shell
    python main.py [installation_id]


## Output

The anonymized DBs (or records if 'installation_id' is provided) are exported to CSV files corresponding to each DB table. For instance, an anonymized 'segments' table generates a segments.csv file in the 'output' directory.

