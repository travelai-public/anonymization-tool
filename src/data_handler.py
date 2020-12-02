# This Python file uses the following encoding: utf-8
import sys, os, logging, csv, coloredlogs, colorlog
import psycopg2
from itertools import *
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from timeit import default_timer as timer
import math



def attribute_validation(dic_of_tables):

    # print(dic_of_tables["segments"])

    new_dic_of_tables={}

    #pd.set_option('display.expand_frame_repr', False);

    # df = pd.read_csv(os.getcwd()+ '/utils/shareable_attributes.csv', header=None, sep='\n')
    # df = df[0].str.split('\s\,\s', expand=True)

    ## Using the current number of atributes... if they changem the range needs to be updated
    df = pd.read_csv(os.getcwd()+ '/utils/shareable_attributes.csv', delimiter=',', names=list(range(15)))

    
    ## index 0 is the table name
    ## index from 1 to 14 is the attribute


    df_transposed = df.T
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed.iloc[1:]

    logging.debug('Attribute information loaded.')


    # # Print the whole DataFrame
    # print(segments)
    # print("------ ------- ------")
    
    # ## Filter per specirfic installation ID
    # print(segments.loc[segments['installation_id'] == '9ef9c89c-ad1b-4890-a1f7-2b7d0931472c'])
    # print(routes)
    # print(gis_legs)
    # #print(dataFrameWaypoints)


    ## Checking the name of the dataframe using the 'name' attribute
    ## segments, routes, gis_legs, waypoints

    logging.debug('Starting to validate de attributes.')
    ## Print just 

    for key, value in dic_of_tables.items():

        tmp_dataframe = pd.DataFrame() 

        


        if key == "segments" and value.name == "segments":
            ## Do logic
            # print(df_transposed.loc[:, ['segments']])

            for index, row in df_transposed.iterrows():
                if row['segments'] in value.columns:
                    logging.debug('%s is valid.',row['segments'])
                    #print(dic_of_tables[key][row['segments']])
                    tmp_dataframe[row['segments']]=dic_of_tables[key][row['segments']]
                    
                else:
                    logging.debug('%s not valid.',row['segments'])
                    ## drop column that is not to share
                    if math.isnan(row['segments']):
                        logging.debug('Found NaN. Ignoring.')

                        ## HERE to continue
                    else:
                        logging.debug('Dropping column.')
                        dic_of_tables[key].drop(columns=[row['segments']])

            tmp_dataframe.name = key
            new_dic_of_tables.update({key:tmp_dataframe})




        elif key == "routes" and value.name == "routes":
            ## Do logic
            ## print(df_transposed.loc[:, ['routes']])
            
            for index, row in df_transposed.iterrows():
                if row['routes'] in value.columns:
                    logging.debug('%s is valid.',row['routes'])
                    #print(dic_of_tables[key][row['routes']])
                    tmp_dataframe[row['routes']]=dic_of_tables[key][row['routes']]
                    
                else:
                    logging.debug('%s not valid.',row['routes'])
                    ## drop column that is not to share
                    if math.isnan(row['routes']):
                        logging.debug('Found NaN. Ignoring.')

                        ## Here to continue
                    else:
                        logging.debug('Dropping column.')
                        dic_of_tables[key].drop(columns=[row['routes']])

            tmp_dataframe.name = key
            new_dic_of_tables.update({key:tmp_dataframe})

        elif key == "gis_legs" and value.name == "gis_legs":
            ## Do logic
            ## print(df_transposed.loc[:, ['gis_legs']])
            
            for index, row in df_transposed.iterrows():
                if row['gis_legs'] in value.columns:
                    logging.debug('%s is valid.',row['gis_legs'])
                    #print(dic_of_tables[key][row['gis_legs']])
                    tmp_dataframe[row['gis_legs']]=dic_of_tables[key][row['gis_legs']]
                    
                else:
                    logging.debug('%s not valid.',row['gis_legs'])
                    ## drop column that is not to share
                    if math.isnan(row['gis_legs']):
                        logging.debug('Found NaN. Ignoring.')

                        ## Here to continue
                    else:
                        logging.debug('Dropping column.')
                        dic_of_tables[key].drop(columns=[row['gis_legs']])

            tmp_dataframe.name = key
            new_dic_of_tables.update({key:tmp_dataframe})

        elif key == "waypoints" and value.name == "waypoints":
            ## Do logic
            ## print(df_transposed.loc[:, ['waypoints']])
            for index, row in df_transposed.iterrows():
                if row['waypoints'] in value.columns:
                    logging.debug('%s is valid.',row['waypoints'])
                    #print(dic_of_tables[key][row['waypoints']])
                    tmp_dataframe[row['waypoints']]=dic_of_tables[key][row['waypoints']]
                    
                else:
                    logging.debug('%s not valid.',row['waypoints'])
                    ## drop column that is not to share
                    if math.isnan(row['waypoints']):
                        logging.debug('Found NaN. Ignoring.')

                        ## Here to continue
                    else:
                        logging.debug('Dropping column.')
                        dic_of_tables[key].drop(columns=[row['waypoints']])

            tmp_dataframe.name = key
            new_dic_of_tables.update({key:tmp_dataframe})

        elif key == "places" and value.name == "places":
            ## Do logic
            ## print(df_transposed.loc[:, ['places']])
            for index, row in df_transposed.iterrows():
                if row['places'] in value.columns:
                    logging.debug('%s is valid.',row['places'])
                    #print(dic_of_tables[key][row['places']])
                    tmp_dataframe[row['places']]=dic_of_tables[key][row['places']]
                    
                else:
                    logging.debug('%s not valid.',row['places'])
                    ## drop column that is not to share
                    try: 
                        if math.isnan(row['places']):
                            logging.debug('Found NaN. Ignoring.')

                            ## Here to continue
                        else:
                            logging.debug('Dropping column.')
                            dic_of_tables[key].drop(columns=[row['places']])
                    except TypeError as e:
                        logging.debug(e)

            tmp_dataframe.name = key
            new_dic_of_tables.update({key:tmp_dataframe})

    # print("-------")
    # print(new_dic_of_tables["segments"])

    #dataFrameSegments.loc[1:3, ['installation_id', 'routes_count','legs_count']]))


    # uniqueInstalID = segments['installation_id'].unique()
    # print('Unique elements in column "installation_id" ')
    # print(uniqueInstalID)

    if "segments" in dic_of_tables:
        print("\n")
        print("Total Instalation IDs (Segments): ",dic_of_tables["segments"].__len__())
        print("Total __Unique__ Instalation IDs (Segments): ",dic_of_tables["segments"]['installation_id'].unique().__len__())
        print("New version total Instalation IDs (Segments): ",new_dic_of_tables["segments"].__len__())
        print("New version total __Unique__ Instalation IDs (Segments): ",new_dic_of_tables["segments"]['installation_id'].unique().__len__())
        print(new_dic_of_tables["segments"].columns)

    if "routes" in dic_of_tables:
        print("\n")
        print("Total Instalation IDs (routes): ",dic_of_tables["routes"].__len__())
        print("Total __Unique__ Instalation IDs (routes): ",dic_of_tables["routes"]['installation_id'].unique().__len__())
        print("New version total Instalation IDs (routes): ",new_dic_of_tables["routes"].__len__())
        print("New version total __Unique__ Instalation IDs (routes): ",new_dic_of_tables["routes"]['installation_id'].unique().__len__())
        print(new_dic_of_tables["routes"].columns)

    if "gis_legs" in dic_of_tables:
        print("\n")
        print("Total Instalation IDs (gis_legs): ",dic_of_tables["gis_legs"].__len__())
        print("Total __Unique__ Instalation IDs (gis_legs): ",dic_of_tables["gis_legs"]['installation_id'].unique().__len__())
        print("New version total Instalation IDs (gis_legs): ",new_dic_of_tables["gis_legs"].__len__())
        print("New version total __Unique__ Instalation IDs (gis_legs): ",new_dic_of_tables["gis_legs"]['installation_id'].unique().__len__())
        print(new_dic_of_tables["gis_legs"].columns)

    if "waypoints" in dic_of_tables:
        print("\n")
        print("Total Instalation IDs (waypoints): ",dic_of_tables["waypoints"].__len__())
        print("Total __Unique__ Instalation IDs (waypoints): ",dic_of_tables["waypoints"]['installation_id'].unique().__len__())
        print("New version total Instalation IDs (waypoints): ",new_dic_of_tables["waypoints"].__len__())
        print("New version total __Unique__ Instalation IDs (waypoints): ",new_dic_of_tables["waypoints"]['installation_id'].unique().__len__())
        print(new_dic_of_tables["waypoints"].columns)

    if "places" in dic_of_tables:
        print("\n")
        print("Total Instalation IDs (places): ",dic_of_tables["places"].__len__())
        print("Total __Unique__ Instalation IDs (places): ",dic_of_tables["places"]['installation_id'].unique().__len__())
        print("New version total Instalation IDs (places): ",new_dic_of_tables["places"].__len__())
        print("New version total __Unique__ Instalation IDs (places): ",new_dic_of_tables["places"]['installation_id'].unique().__len__())
        print(new_dic_of_tables["places"].columns)

    return new_dic_of_tables


