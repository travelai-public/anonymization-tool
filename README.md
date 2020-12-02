# Anonymization Tool

V0.7


## Installation Instructions

Using PIP environment, the anonymization tool will automatically install and setup all the necessary dependencies. 

Be sure to set and export the variables in your virtual environemnt. 

### Expected Travels Format

![Travel Data Format](/images/travelai_travel_format.png)

The anonymization tool expect travels data in specific format, using five different travel object definitions:

#### Segments

#### Routes

#### GIS_Legs

#### Waypoints

#### Places


### Database Settings

The software will automatically load the settings and connect to the DB according to the following environment variables:

	DB_USERNAME
	DB_HOST
	DB_PORT
	DB_NAME

The anonymization tool will automatically revert to development configuration if no such settings can be found in the enviroment. 

### Database Format

The software expects the following structure for the input database:

#### public.segments
- id,  
- installation_id,  
- start_ts,  
- end_ts,  
- routes_count,  
- legs_count,  
- gaps_count,  
- start_place_id,  
- end_place_id,  
- gislegs_count  


#### public.routes
- id, 
- installation_id,
- start_ts,
- end_ts,
- distance,
- gis_distance,
- duration,
- start_place,
- end_place,
- start_dwell,
- end_dwell,
- data_quality,
- match_confidence,
- segment_id


#### public.gis_legs
- id,
- installation_id,
- start_ts,
- end_ts,
- transport_mode,
- distance,
- duration,
- match_confidence,
- route_id,
- first_location,
- last_location


#### public.waypoints
- installation_id,
- route_id,
- gisleg_id,
- timestamp,
- transport_mode,
- location,
- accuracy,
- vaccuracy,
- speed,
- provider


#### public.places
- timestamp,
- id,
- installation_id,
- location,
- dwelltime_sum,
- dwelltime_percentage,
- dwelltime_rank,
- label,
- placeloc_strength,
- first_dwell_starttime,
- last_dwell_endtime,
- place_reverse_goecode_id



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

