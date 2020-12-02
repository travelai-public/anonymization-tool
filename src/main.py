# This Python file uses the following encoding: utf-8
import sys, os, logging, csv, coloredlogs, colorlog
import psycopg2
from itertools import *
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from timeit import default_timer as timer

from db_connector import retrieve_db_data
from data_handler import attribute_validation
from utils.metrics import correlation_of_all_dataframes, show_graphics,retrive_min_max_values
from anonymizer import *

import multiprocessing
from multiprocessing import Process ## first try
from multiprocessing import Pool
from multiprocessing import Manager
from multiprocessing.pool import ThreadPool ## second try



## Importing Metrics from Scikit learn
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#log_level = logging.INFO
log_level = logging.DEBUG


## DB Settings
if 'DB_USERNAME' and 'DB_HOST' and 'DB_PORT' and 'DB_NAME' in os.environ:
    DB_USERNAME=os.environ.get('DB_USERNAME')
    DB_HOST=os.environ.get('DB_HOST')
    DB_PORT=os.environ.get('DB_PORT')
    DB_NAME=os.environ.get('DB_NAME')
    logging.info('Loaded ENVVAR: DB_USERNAME, DB_HOST, DB_PORT and DB_NAME')
else:
    DB_USERNAME='paulosilva'
    DB_HOST='127.0.0.1'
    DB_PORT='5433'
    DB_NAME='tp2'
    logging.info('Loaded default settings. DB_USERNAME=%s, DB_HOST=%s, DB_PORT=%s and DB_NAME=%s',DB_USERNAME, DB_HOST, DB_PORT, DB_NAME)


def setup_logging(log_level=logging.INFO):
    """Set up the logging."""
    logging.basicConfig(level=log_level)
    #fmt = ("%(asctime)s %(levelname)s (%(threadName)s) " "[%(name)s] %(message)s")
    fmt = ("%(asctime)s %(process)d %(levelname)s anon_tool : %(message)s")
    colorfmt = "%(log_color)s{}%(reset)s".format(fmt)
    #datefmt = '%Y-%m-%d %H:%M:%S'
    datefmt='%s'

    # Suppress overly verbose logs from libraries that aren't helpful
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    try:
        from colorlog import ColoredFormatter
        logging.getLogger().handlers[0].setFormatter(ColoredFormatter(
            colorfmt,
            datefmt=datefmt,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        ))
    except ImportError:
        pass

    logger = logging.getLogger('')
    logger.setLevel(log_level)


setup_logging(log_level)   






if __name__ == '__main__':


    ## Example installation IDs for single anonymization

    ## python main.py 12db437b-0782-4ad8-abda-2bb5055570c8  // 4 routes // 2 legs
    ## python main.py c3a6ccc6-a255-47e3-9035-95b8a9554514  // 0 routes // 4 legs
    ## python main.py 0db2f591-abd6-45fa-a3a1-68619e2bc11c  // 3 routes // 1 leg
    ## python main.py c8632816-c3f3-45b5-b50a-9dfb54e574e5  // 0 routes // 0 legs
    ## python main.py 8acc8a5f-1f05-4005-bfdb-787be023cf19 zac android
    ## python main.py b60ac3e9-b96f-4257-8a35-c5e1339b6130 zac apple


    





    logger = logging.getLogger(__name__)


    # USAGE: python main.py [installation_id]

    installation_id = None
    try:
        installation_id = sys.argv[1]
        logging.info("""Succesfully got 'installation_id' from user input: %s.""",installation_id)

    except IndexError:
        logging.info("""'installation_id' not provided. Proceeding with global anonymization.""")




    logging.info('Initializing...')

    # # Create an engine instance
    logging.info('Creating DB Engine...')
    # alchemyEngine = create_engine('postgresql+psycopg2://paulosilva:@127.0.0.1:5433/tp2', pool_recycle=3600)
    alchemyEngine = create_engine('postgresql+psycopg2://' + DB_USERNAME + ':@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME, pool_recycle=3600)
    

    # Connect to PostgreSQL server
    logging.info('Connecting to DB...')
    dbConnection = alchemyEngine.connect()
    

    # Keep Data
    logging.info('Retrieving data...')
    dic_of_tables = retrieve_db_data(dbConnection)
    

    # Close the database connection
    dbConnection.close();
    logging.info('Data succesfully loaded.')


    # for key,value in dic_of_tables.items():
    #     print("Table: ",key)
    #     print(value)
    #     input()


        
    #segments, routes, gis_legs = retrieve_db_data(dbConnection)
    #segments, routes, gis_legs, waypoints = retrieve_db_data(dbConnection)

    
    clean_dic_of_tables = attribute_validation(dic_of_tables)

    # correlation = dic_of_tables["segments"].corr()
    # print(correlation)


    # show_graphics(correlation_of_all_dataframes(dic_of_tables))
    # show_graphics(correlation_of_all_dataframes(clean_dic_of_tables))

    ## description of dataframe
    print(clean_dic_of_tables)
    # print(dic_of_tables["segments"].describe())




    ## Just to het the min and max values of an attribute
    min, max = retrive_min_max_values(clean_dic_of_tables["segments"]["gislegs_count"])

    


    if installation_id == None:

        ## Set list of processes
        procs = []    


        p1 = Process(target=anonymization, args=(clean_dic_of_tables["segments"],))
        p1.start()
        procs.append(p1)

        # anonymous_segments, optimal_node = anonymization(clean_dic_of_tables["segments"])
        # print(anonymous_segments)
        # print(optimal_node)

        print("------------------")

        p2 = Process(target=anonymization, args=(clean_dic_of_tables["routes"],))
        p2.start()
        procs.append(p2)

        # anonymous_routes, optimal_node = anonymization(clean_dic_of_tables["routes"])
        # print(anonymous_routes)
        # print(optimal_node)

        print("------------------")

        p3 = Process(target=anonymization, args=(clean_dic_of_tables["gis_legs"],))
        p3.start()
        procs.append(p3)

        # anonymous_legs, optimal_node = anonymization(clean_dic_of_tables["gis_legs"])
        # print(anonymous_legs)
        # print(optimal_node)

        print("------------------")

        try:

            p4 = Process(target=anonymization, args=(clean_dic_of_tables["waypoints"],))
            p4.start()
            procs.append(p4)
        except Exception as e:
            logging.error('%s not loaded in this execution...', e)

        ## Cleaning up...
        for p in procs:
             p.join()

        # anonymous_waypoints, optimal_node = anonymization(clean_dic_of_tables["waypoints"])
        # print(anonymous_waypoints)
        # print(optimal_node)
            
        #print(correlation)

    else:
        logging.info('Gathering installation_id details...')

        
        ## filter_by_install_id(clean_dic_of_tables,installation_id)

        single_anonymizationV2(filter_by_install_id(clean_dic_of_tables,installation_id))


    logging.info('Closing...')




    

