# This Python file uses the following encoding: utf-8
import sys, os, logging, csv, coloredlogs, colorlog

## Importing Crowds
import pandas as pd
from crowds.kanonymity.ola import anonymize
from crowds.kanonymity.information_loss import dm_star_loss
from crowds.kanonymity.generalizations import GenRule

from utils.metrics import *
import random 

from shapely.geometry import Point

import datetime

import warnings
warnings.filterwarnings("ignore")


if 'K_ANON' and 'SUPPRESION' in os.environ:
    K_ANON=os.environ.get('K_ANON')
    SUPPRESION=os.environ.get('SUPPRESION')
    logging.info('Loaded ENVVAR: K_ANON and SUPPRESION')
else:
    with open("settings", "r") as f:
        settings = f.readlines()
        K_ANON, SUPPRESION = [d.split('=')[1].split('\n')[0] for d in settings]
        logging.info('Loaded settings. K=%s and max_suppression%s',K_ANON,SUPPRESION)

peaks = {}

try:
    with open("peak_times", "r") as f:
        for line in f:
            (key, value) = line.split('=')
            peaks[key] = value.rstrip('\n')
        logging.info('Loaded peak times.')
except Exception as e:
    logging.info("Not able to load peak times. Setting 7-9am and 5-7pm as peak times for every day.")

# print(peaks)
# input()

## The rules defined below are for now generic and mostly categorical (except timestmap start and end). 
## This needs to be updated in order to:
## - accomodate current min and max values;
## - shift from categorical to discrete representation;
## - address the GEO fields and performing the specific transformations.


OBFUSCATION_RADIUS = 0.5


#pseudonymization of installation_id (example)
installation_id = {
    "f0b30cbf-9aa1-4426-98ce-beb3cd77b450": 1,
    "dd0bac0c-0b15-45b9-91c6-e183890b8268": 2,
    "0c8b420b-ce16-49f7-ba1a-53c46179229f": 3,
    "76601baf-2fc7-4304-8370-c16a907b8644": 4,
    "0c8b420b-ce16-49f7-ba1a-53c46179229f": 5,
    "9ef9c89c-ad1b-4890-a1f7-2b7d0931472c": 6,
    "c3a6ccc6-a255-47e3-9035-95b8a9554514": 7,
    "0db2f591-abd6-45fa-a3a1-68619e2bc11c": 8,
    "12db437b-0782-4ad8-abda-2bb5055570c8": 9
}

## this is to test

## need to load all the IDs, apply pseudonymization and export the mappings


def generalize_installation_id(value):

    ## Insert logic to retrieve data from dic and apply change

    try:
        return installation_id[value]
    except:
        return "test_id"


def generalize_start_ts(value):
    return value + 3 * 60 * 60

def generalize_end_ts(value):
    return value + 4 * 60 * 60

def generalize_distance(value):

    ## To update with values from min and max for each column


    if value <= 100:
        return 'very short'
    if value > 100 and value <= 500:
        return 'short'
    if value > 500 and value <= 1500:
        return 'bellow normal'
    if value > 1500 and value <= 5000:
        return 'normal'
    if value > 5000 and value <= 8500:
        return 'above normal'
    if value > 8500 and value <= 10000:
        return 'long'
    if value > 10000:
        return 'very long'

def generalize_distance_discrete(value):

    ## To update with values from min and max for each column

    deviation = 5

    if value <= 100:
        return value + deviation
    ##  TO DO 


def generalize_gis_distance(value):

    ## To update with values from min and max for each column

    if value <= 100:
        return 'very short'
    if value > 100 and value <= 500:
        return 'short'
    if value > 500 and value <= 1500:
        return 'bellow normal'
    if value > 1500 and value <= 5000:
        return 'normal'
    if value > 5000 and value <= 8500:
        return 'above normal'
    if value > 8500 and value <= 10000:
        return 'long'
    if value > 10000:
        return 'very long'

def generalize_gis_distance_discrete(value):

    ## To update with values from min and max for each column
    
    deviation = 5

    if value <= 100:
        return value + deviation
    ##  TO DO 



def generalize_duration(value):

    ## To update with values from min and max for each column

    if value <= 5000:
        return 'very short'
    if value > 5000 and value <= 50000:
        return 'short'
    if value > 50000 and value <= 103491:
        return 'bellow normal'
    if value > 103491 and value <= 1034919:
        return 'normal'
    if value > 1034919 and value <= 10349198:
        return 'above normal'
    if value > 10349198 and value <= 103491980:
        return 'long'
    if value > 103491980:
        return 'very long'

def generalize_duration_discrete(value):

    ## To update with values from min and max for each column

    deviation = 5

    if value <= 100:
        return value + deviation
    ##  TO DO 



# def generalize_start_place(value):
    # TO DO 
    
# def generalize_end_place(value):
#     # TO DO

def generalize_first_location(value):
    print("Type first location: ", type(value))
    print("Value first_location: ", value)
    if value != None:
        coord = hex_to_coord(value)
                    
        ## Moving approximatelly 500m 
        distance=0.005
        angle_degrees = 45

        new_x = coord.x + distance * math.cos(angle_degrees * math.pi / 180)
        new_y = coord.y + distance * math.sin(angle_degrees * math.pi / 180)


        return coord_to_hex(Point(new_x, new_y))

    else:
        return 0

def generalize_last_location(value):
    print("Type last location: ", type(value))
    print("Value last_location: ", value)
    if value != None:

        coord = hex_to_coord(value)
                        
        ## Moving approximatelly 500m 
        distance=0.005
        angle_degrees = 45

        new_x = coord.x + distance * math.cos(angle_degrees * math.pi / 180)
        new_y = coord.y + distance * math.sin(angle_degrees * math.pi / 180)


        return coord_to_hex(Point(new_x, new_y))

    else:
        return 0

def generalize_timestamp(value):
    if value <= 5000:
        return 'very short'
    if value > 5000 and value <= 50000:
        return 'short'
    if value > 50000 and value <= 103491:
        return 'bellow normal'
    if value > 103491 and value <= 1034919:
        return 'normal'
    if value > 1034919 and value <= 10349198:
        return 'above normal'
    if value > 10349198 and value <= 103491980:
        return 'long'
    if value > 103491980:
        return 'very long'

def generalize_timestamp_discrete(value):
    

    ## To update with values from min and max for each column

    deviation = 5

    if value <= 100:
        return value + deviation
    ##  TO DO 


def generalize_location(value):
    print("Type location: ", type(value))
    print("Value location: ", value)
    if value != None:
        print("Enter in location gen.")
        coord = hex_to_coord(value)
                        
        ## Moving approximatelly 500m 
        distance=0.005
        angle_degrees = 45

        new_x = coord.x + distance * math.cos(angle_degrees * math.pi / 180)
        new_y = coord.y + distance * math.sin(angle_degrees * math.pi / 180)


        return coord_to_hex(Point(new_x, new_y))
    else:
        return 0

# def generalize_accuracy(value):
#     # TO DO

def generalize_speed(value):

    ## To update with values from min and max for each column

    if value <= 5:
        return 'very slow'
    if value > 5 and value <= 30:
        return 'slow'
    if value > 30 and value <= 80:
        return 'normal'
    if value > 80 and value <= 130:
        return 'fast'
    if value > 130:
        return 'very fast'

def generalize_speed_discrete(value):

    ## To update with values from min and max for each column

    deviation = 1

    if value <= 5:
        return value + deviation
    ##  TO DO 


generalization_rules_segments = {


    # 'installation_id': GenRule([]), # 1-level generalization
    # 'id': GenRule([]), # 1-levels generalization
    'start_ts': GenRule([generalize_start_ts]), # 1-levels generalization
    'end_ts': GenRule([generalize_end_ts]), # 1-levels generalization
    'routes_count': GenRule([]), # 1-levels generalization
    'legs_count': GenRule([]), # 1-levels generalization
    'gaps_count': GenRule([]), # 1-levels generalization
    'start_place_id': GenRule([]), # 1-levels generalization
    'end_place_id': GenRule([]), # 1-levels generalization
    'gislegs_count': GenRule([]), # 1-levels generalization
}

generalization_rules_routes = {


    # 'installation_id': GenRule([]), # 1-level generalization
    # 'id': GenRule([]), # 1-levels generalization
    'start_ts': GenRule([generalize_start_ts]), # 1-levels generalization
    'end_ts': GenRule([generalize_end_ts]), # 1-levels generalization
    'distance': GenRule([generalize_distance]), # 1-levels generalization
    'gis_distance': GenRule([generalize_gis_distance]), # 1-levels generalization
    'duration': GenRule([generalize_duration]), # 1-levels generalization
    'start_place': GenRule([]), # 1-levels generalization
    'end_place': GenRule([]), # 1-levels generalization
    'start_dwell': GenRule([]), # 1-levels generalization
    'end_dwell': GenRule([]), # 1-levels generalization
    'data_quality': GenRule([]), # 1-levels generalization
    'match_confidence': GenRule([]), # 1-levels generalization
    # 'segment_id': GenRule([]), # 1-levels generalization
}

generalization_rules_gis_legs = {


    # 'installation_id': GenRule([]), # 1-level generalization
    # 'id': GenRule([]), # 1-levels generalization
    'start_ts': GenRule([generalize_start_ts]), # 1-levels generalization
    'end_ts': GenRule([generalize_end_ts]), # 1-levels generalization
    'transport_mode': GenRule([]), # 1-levels generalization
    'distance': GenRule([generalize_distance]), # 1-levels generalization
    'duration': GenRule([generalize_duration]), # 1-levels generalization
    'match_confidence': GenRule([]), # 1-levels generalization
    # 'route_id': GenRule([]), # 1-levels generalization
    'first_location': GenRule([generalize_first_location]), # 2-levels generalization
    'last_location': GenRule([generalize_last_location]), # 2-levels generalization
}

generalization_rules_waypoints = {


    # 'installation_id': GenRule([]), # 1-level generalization
    # 'route_id': GenRule([]), # 1-levels generalization
    # 'gisleg_id': GenRule([]), # 1-levels generalization
    'timestamp': GenRule([generalize_timestamp]), # 2-levels generalization
    'transport_mode': GenRule([]), # 1-levels generalization
    # 'location': GenRule([generalize_location]), # 2-levels generalization
    'accuracy': GenRule([]), # 1-levels generalization
    'vaccuracy': GenRule([]), # 1-levels generalization
    'speed': GenRule([generalize_speed]), # 2-levels generalization
    'provider': GenRule([]), # 1-levels generalization
}

def anonymization(dataframe):

    file_name = os.getcwd()+ '/output/'

    logging.info('K=%s Supression=%s',K_ANON,SUPPRESION)

    if dataframe.name == "segments":
        logging.debug('Starting anonymization of: %s',dataframe.name)
        logging.debug('Columns in Dataframe: %s',dataframe.columns)
        anonymous_list, optimal_node = anonymize(dataframe, generalization_rules=generalization_rules_segments, k=int(K_ANON), max_sup=float(SUPPRESION), info_loss=dm_star_loss)
        print(anonymous_list)

        gfg_csv_data = anonymous_list.to_csv(file_name + 'segments.csv', index = True) 
        print('\nCSV String:\n', gfg_csv_data) 
        return 
    
    elif dataframe.name == "routes":
        logging.debug('Starting anonymization of: %s',dataframe.name)
        logging.debug('Columns in Dataframe: %s',dataframe.columns)
        anonymous_list, optimal_node = anonymize(dataframe, generalization_rules=generalization_rules_routes, k=int(K_ANON), max_sup=float(SUPPRESION), info_loss=dm_star_loss)
        print(anonymous_list)

        gfg_csv_data = anonymous_list.to_csv(file_name + 'routes.csv', index = True) 
        print('\nCSV String:\n', gfg_csv_data) 

        return 
    
    elif dataframe.name == "gis_legs":
        logging.debug('Starting anonymization of: %s',dataframe.name)
        logging.debug('Columns in Dataframe: %s',dataframe.columns)
        anonymous_list, optimal_node = anonymize(dataframe, generalization_rules=generalization_rules_gis_legs, k=int(K_ANON), max_sup=float(SUPPRESION), info_loss=dm_star_loss)
        print(anonymous_list)
        
        gfg_csv_data = anonymous_list.to_csv(file_name + 'gis_legs.csv', index = True) 
        print('\nCSV String:\n', gfg_csv_data) 
        
        return 
    
    elif dataframe.name == "waypoints":
        logging.debug('Starting anonymization of: %s',dataframe.name)
        logging.debug('Columns in Dataframe: %s',dataframe.columns)
        anonymous_list, optimal_node = anonymize(dataframe, generalization_rules=generalization_rules_waypoints, k=int(K_ANON), max_sup=float(SUPPRESION), info_loss=dm_star_loss)
        print(anonymous_list)
        
        gfg_csv_data = anonymous_list.to_csv(file_name + 'waypoints.csv', index = True) 
        print('\nCSV String:\n', gfg_csv_data) 
        
        return 
    
    else:
        logging.debug('No valid dataframe provided...')
        return None


def time_in_range(start, end, to_check):
    ### Returns true if **to_check** is in the range [start, end]
    if start <= end:
        return start <= to_check <= end
    else:
        return start <= to_check or to_check <= end



### gets timestamp (in milliseconds)
def check_timestamp(timestamp):
    ## from 0 to 6
    weekday = datetime.datetime.fromtimestamp(int(timestamp/1000)).weekday()
    hour_min_sec = datetime.datetime.fromtimestamp(int(timestamp/1000)).time()

    if weekday == 0:
        am_start = datetime.datetime.strptime(peaks["MONDAY_AM_START"],'%H:%M').time()
        am_end = datetime.datetime.strptime(peaks["MONDAY_AM_END"],'%H:%M').time()
        pm_start = datetime.datetime.strptime(peaks["MONDAY_AM_START"],'%H:%M').time()
        pm_end = datetime.datetime.strptime(peaks["MONDAY_AM_END"],'%H:%M').time()
    elif weekday == 1:
        am_start = datetime.datetime.strptime(peaks["TUESDAY_AM_START"],'%H:%M').time()
        am_end = datetime.datetime.strptime(peaks["TUESDAY_AM_END"],'%H:%M').time()
        pm_start = datetime.datetime.strptime(peaks["TUESDAY_AM_START"],'%H:%M').time()
        pm_end = datetime.datetime.strptime(peaks["TUESDAY_AM_END"],'%H:%M').time()
    elif weekday == 2:
        am_start = datetime.datetime.strptime(peaks["WEDNESDAY_AM_START"],'%H:%M').time()
        am_end = datetime.datetime.strptime(peaks["WEDNESDAY_AM_END"],'%H:%M').time()
        pm_start = datetime.datetime.strptime(peaks["WEDNESDAY_AM_START"],'%H:%M').time()
        pm_end = datetime.datetime.strptime(peaks["WEDNESDAY_AM_END"],'%H:%M').time()
    elif weekday == 3:
        am_start = datetime.datetime.strptime(peaks["THURSDAY_AM_START"],'%H:%M').time()
        am_end = datetime.datetime.strptime(peaks["THURSDAY_AM_END"],'%H:%M').time()
        pm_start = datetime.datetime.strptime(peaks["THURSDAY_AM_START"],'%H:%M').time()
        pm_end = datetime.datetime.strptime(peaks["THURSDAY_AM_END"],'%H:%M').time()
    elif weekday == 4:
        am_start = datetime.datetime.strptime(peaks["FRIDAY_AM_START"],'%H:%M').time()
        am_end = datetime.datetime.strptime(peaks["FRIDAY_AM_END"],'%H:%M').time()
        pm_start = datetime.datetime.strptime(peaks["FRIDAY_AM_START"],'%H:%M').time()
        pm_end = datetime.datetime.strptime(peaks["FRIDAY_AM_END"],'%H:%M').time()
    elif weekday == 5:
        am_start = datetime.datetime.strptime(peaks["SATURDAY_AM_START"],'%H:%M').time()
        am_end = datetime.datetime.strptime(peaks["SATURDAY_AM_END"],'%H:%M').time()
        pm_start = datetime.datetime.strptime(peaks["SATURDAY_AM_START"],'%H:%M').time()
        pm_end = datetime.datetime.strptime(peaks["SATURDAY_AM_END"],'%H:%M').time()
    elif weekday == 6:
        am_start = datetime.datetime.strptime(peaks["SUNDAY_AM_START"],'%H:%M').time()
        am_end = datetime.datetime.strptime(peaks["SUNDAY_AM_END"],'%H:%M').time()
        pm_start = datetime.datetime.strptime(peaks["SUNDAY_AM_START"],'%H:%M').time()
        pm_end = datetime.datetime.strptime(peaks["SUNDAY_AM_END"],'%H:%M').time()

    # start = datetime.time(15, 10, 0)
    # end = datetime.time(17, 0, 0) 


    # ### For debugging 
    # print(am_start)
    # print(am_end)
    # print(hour_min_sec)
    # input()

    if time_in_range(am_start, am_end, hour_min_sec):
        if weekday == 5 or weekday == 6:
            return "Weekend AM Peak"
        else:
            return "Week AM Peak"
    elif time_in_range(pm_start, pm_end, hour_min_sec):
        if weekday == 5 or weekday == 6:
            return "Weekend PM Peak"
        else:
            return "Week PM Peak"
    else:
        return "Regular"


    # print(time_in_range(start, end, hour_min_sec))

    # print(time_in_range(start, end, datetime.time(18, 30, 0)))

    # ## Getting hour from peak times:
    # hour = datetime.datetime.strptime(peaks["MONDAY_AM_START"],'%H:%M').time()

    # print(datetime.datetime.strptime(peaks["MONDAY_AM_START"],'%H:%M').time())
    # input()

    # print(time_in_range(start, end, hour))
    # start = datetime.time(6, 10, 0)
    # end = datetime.time(17, 0, 0)
    # print(time_in_range(start, end, hour))

    # input()


def filter_by_install_id(dic_of_tables, installation_id):

    ## Key is the name of the table
    ## Value is the dataframe that refers to the table

    install_id_dic_of_tables = {}


    ## get data from this installation ID
    for key,value in dic_of_tables.items():


        if key == "segments":
            logging.debug("Filtering segments...")

            tmp_dataframe = pd.DataFrame()

            tmp_dataframe = value.query('installation_id == @installation_id')

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "routes":
            logging.debug("Filtering routes...")

            tmp_dataframe = pd.DataFrame()

            tmp_dataframe = value.query('installation_id == @installation_id')

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "gis_legs":
            logging.debug("Filtering gis_legs...")

            tmp_dataframe = pd.DataFrame()

            tmp_dataframe = value.query('installation_id == @installation_id')

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "waypoints":
            logging.debug("Filtering waypoints...")

            tmp_dataframe = value.query('installation_id == @installation_id')
            # print(tmp_dataframe)
            # print(len(tmp_dataframe.index))
            # input()

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "places":
            ## Contains: route_id and gisleg_id

            logging.debug("Processing places...")

            tmp_dataframe = value.query('installation_id == @installation_id')


            


            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})

        else:
            logging.debug('Supported tables were not found. Please try again.')


    return(install_id_dic_of_tables)






def single_anonymization(dic_of_tables):
    ## TO DO


    install_id_dic_of_tables = {}

    for key, value in dic_of_tables.items():
        print(key)
        # in case I need to print it all....
        print(value.to_string())

        # print(value)

        if key == "segments":
            logging.debug("Processing segments...")

            tmp_dataframe = pd.DataFrame()

            ## tmp_dataframe = value.query('start_ts == @installation_id')

            max_routes = 0
            for segment_id in value["id"]:

                #print(segment_id)
                #print("Size: ",len(dic_of_tables["routes"].query('segment_id == @segment_id')))
                if len(dic_of_tables["routes"].query('segment_id == @segment_id')) > max_routes:
                    max_routes+=1

                #print(dic_of_tables["routes"].query('segment_id == @segment_id'))

            print("Max routes: ",max_routes)
            input()

  
                
                # for item in tmp.iterrows():
                #     print(item[])
                #     input()
                # input()


            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "routes":
            ## Contains: segment_id
            logging.debug("Processing routes...")

            tmp_dataframe = pd.DataFrame()

            max_legs = 0
            max_waypoints = 0
            for route_id in value["id"]:
                # print(route_id)
                # print("Size: ",len(dic_of_tables["gis_legs"].query('route_id == @route_id')))
                if len(dic_of_tables["gis_legs"].query('route_id == @route_id')) > max_legs:
                    max_legs+=1


                tmp_dataframe=dic_of_tables["waypoints"].query('route_id == @route_id')
                print(tmp_dataframe)
                
                # for row in tmp_dataframe.iterrows():
                #     print(row)
                #     # print("Milliseconds :", row["timestamp"])
                #     # print("Seconds :", row["timestamp"]/1000)

                
                for row in tmp_dataframe.itertuples():
                    #print(row.timestamp/1000)
                    print(datetime.datetime.fromtimestamp(int(row.timestamp/1000)).isoformat())
                    #print(row.Index)



                # print(dic_of_tables["gis_legs"].query('route_id == @route_id'))
            
            print("Max legs: ",max_legs)
            input()




            tmp_dataframe = value.query('installation_id == @installation_id')

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "gis_legs":
            ## Contains: route_id


            logging.debug("Processing gis_legs...")

            tmp_dataframe = pd.DataFrame()

            tmp_dataframe = value.query('installation_id == @installation_id')

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "waypoints":
            ## Contains: route_id and gisleg_id

            logging.debug("Processing waypoints...")

            tmp_dataframe = value.query('installation_id == @installation_id')


            


            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        else:
            logging.debug('Supported tables were not found. Please try again.')




        ## Segments
        ## check start_ts
        ## check end_ts

        ## Routes
        ## check start_ts
        ## check end_ts

        ## Gisl_egs
        ## check start_ts
        ## check end_ts

        ## Waypoints
        ## timestamp




def single_anonymizationV2(dic_of_tables):

    install_id_dic_of_tables = {}

    file_name = os.getcwd()+ '/output/individual/'

        

    for key, value in dic_of_tables.items():
        # print(key)
        ### in case I need to print it all....
        # print(value.to_string())
        ### in case I need to print just head tail....
        # print(value)

        if key == "segments":
            logging.debug("Processing segments...")

            tmp_dataframe = pd.DataFrame()

            ## tmp_dataframe = value.query('start_ts == @installation_id')

            max_routes = 0
            for segment_id in value["id"]:

                #print(segment_id)
                #print("Size: ",len(dic_of_tables["routes"].query('segment_id == @segment_id')))
                if len(dic_of_tables["routes"].query('segment_id == @segment_id')) > max_routes:
                    max_routes+=1

                #print(dic_of_tables["routes"].query('segment_id == @segment_id'))

            print("Max routes: ",max_routes)

            gfg_csv_data = value.to_csv(file_name + 'segments.csv', index = True, mode='a') 
            # print('\nCSV Segments...\n', gfg_csv_data) 
            logging.info("Writing to CSV file: Segments")

  
                
                # for item in tmp.iterrows():
                #     print(item[])
                #     input()
                # input()


            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "routes":
            ## Contains: segment_id
            logging.debug("Processing routes...")

            tmp_dataframe = pd.DataFrame()

            max_legs = 0
            max_waypoints = 0
            n=len(value["id"])
            index=0
            for route_id in value["id"]:
                ## for progress bar
                index+=1
                j = (index + 1) / n

                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%% \n" % ('='*int(20*j), 100*j))
                sys.stdout.flush()





                # print(route_id)
                # print("Size: ",len(dic_of_tables["gis_legs"].query('route_id == @route_id')))
                if len(dic_of_tables["gis_legs"].query('route_id == @route_id')) > max_legs:
                    max_legs+=1


                tmp_dataframe=dic_of_tables["waypoints"].query('route_id == @route_id')


                ## change attribute type
                tmp_dataframe['timestamp'] = tmp_dataframe['timestamp'].astype(str)
                # tmp_dataframe.at[row.Index,'location']

                #print(tmp_dataframe)
                
                # for row in tmp_dataframe.iterrows():
                #     print(row)
                #     # print("Milliseconds :", row["timestamp"])
                #     # print("Seconds :", row["timestamp"]/1000)

                

                ## Generate a random direction
                angle_degrees = random.randint(1,181)
                #logging.debug("Direction: %d" % angle_degrees)

                order_count=0
                for row in tmp_dataframe.itertuples():
                    order_count+=1



                    # print(row)
                    # iso = datetime.datetime.fromtimestamp(int(row.timestamp/1000)).isoformat()
                    # weekday = datetime.datetime.today().weekday()
                    # today_weekday = datetime.datetime.today().weekday()

                    # new_timestamp = check_time(row.timestamp)
                

                    ## print(type(row.location))
                    ## String

                    coord = hex_to_coord(row.location)

                    ## To check the original coordinates
                    # print("X: ", coord.x)
                    # print("Y: ", coord.y)




                    ## Moving approximatelly 500m 
                    distance=0.005

                    new_x = coord.x + distance * math.cos(angle_degrees * math.pi / 180)
                    new_y = coord.y + distance * math.sin(angle_degrees * math.pi / 180)

                    ## To check the offset distance
                    # print("Distance (KMs): %.3f" % calc_distance([coord.x,coord.y], [new_x,new_y]))

                    ## To check the length
                    # print("Length: ",coord_length([coord.x,coord.y], [new_x,new_y]))


                    ## To check new coordinates... 
                    # print(new_x)
                    # print(new_y)


                    ## ----------------------------------------------------------------------------------------------
                    ## Set new values for the attributes....
                    tmp_dataframe.at[row.Index,'location'] = coord_to_hex(Point(new_x, new_y))
                    tmp_dataframe.at[row.Index,'timestamp'] = str(order_count)+ '_' + check_timestamp(int(row.timestamp))



                    # print("Encoded: ",coord_to_hex(Point(new_x, new_y)))

                    ## To check the updated dataframe...
                    # print(tmp_dataframe)


                    # input()

                # input()
                if os.path.isfile(file_name + 'waypoints.csv'):
                    gfg_csv_data = tmp_dataframe.to_csv(file_name + 'waypoints.csv', index = True, mode='a', header=None) 
                else:
                    gfg_csv_data = tmp_dataframe.to_csv(file_name + 'waypoints.csv', index = True, mode='a')
                # print('\nCSV Waypoints added...\n', gfg_csv_data)
                # logging.info("Writing to CSV file: Waypoints") 

                # input()

            logging.info("Write to CSV file complete: Waypoints") 
            gfg_csv_data = value.to_csv(file_name + 'routes.csv', index = True,mode='a') 
            # print('\nCSV Routes...\n', gfg_csv_data) 
            logging.info("Writing to CSV file: Routes")



                # print(dic_of_tables["gis_legs"].query('route_id == @route_id'))
            
            print("Max legs: ",max_legs)


            tmp_dataframe = value.query('installation_id == @installation_id')

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        elif key == "gis_legs":
            ## Contains: route_id


            logging.debug("Processing gis_legs...")

            tmp_dataframe = pd.DataFrame()

            gfg_csv_data = value.to_csv(file_name + 'gis_legs.csv', index = True, mode='a') 
            #print('\nCSV Gis_legs...\n', gfg_csv_data) 
            logging.info("Writing to CSV file: Gis legs")

            tmp_dataframe = value.query('installation_id == @installation_id')

            tmp_dataframe.name = key
            install_id_dic_of_tables.update({key:tmp_dataframe})


        ## Not needed at the moment.... 

        # elif key == "waypoints":
        #     ## Contains: route_id and gisleg_id

        #     logging.debug("Processing waypoints...")

        #     tmp_dataframe = value.query('installation_id == @installation_id')

        #     tmp_dataframe.name = key
        #     install_id_dic_of_tables.update({key:tmp_dataframe})



        ## Not needed at the moment.... 

        # elif key == "places":
        #     ## Contains: route_id and gisleg_id

        #     logging.debug("Processing places...")

        #     tmp_dataframe = value.query('installation_id == @installation_id')



        #     tmp_dataframe.name = key
        #     install_id_dic_of_tables.update({key:tmp_dataframe})

        else:
            logging.debug('Supported tables were not found. Please try again.')




        ## Segments
        ## check start_ts
        ## check end_ts

        ## Routes
        ## check start_ts
        ## check end_ts

        ## Gisl_egs
        ## check start_ts
        ## check end_ts

        ## Waypoints
        ## timestamp















