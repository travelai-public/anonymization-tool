# This Python file uses the following encoding: utf-8
import sys, os, logging, csv, coloredlogs, colorlog
import psycopg2
from itertools import *
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from timeit import default_timer as timer

## Importing Crypto Numerics library


def retrieve_db_data(dbConnection):

    ## ORDER IS segments -> routes -> gislegs -> waypoints

    dic_of_tables = {}


    # Read data from PostgreSQL database table and load into a DataFrame instance
    # Segments
    start_time = timer()
    dataFrameSegments = pd.read_sql("select * from public.segments WHERE obsolete='false'", dbConnection);
    dataFrameSegments.name = "segments"
    end_time = timer()
    dic_of_tables.update({"segments":dataFrameSegments})
    segments= end_time - start_time

    # Routes
    start_time = timer()
    dataFrameRoutes = pd.read_sql("select * from public.routes WHERE obsolete='false'", dbConnection);
    dataFrameRoutes.name = "routes"
    end_time = timer()
    #dic_of_tables.append(dataFrameRoutes)
    dic_of_tables.update({"routes":dataFrameRoutes})
    routes= end_time - start_time

    # Gis_legs
    start_time = timer()
    dataFrameGis_legs = pd.read_sql("select * from public.gis_legs WHERE obsolete='false'", dbConnection);
    dataFrameGis_legs.name = "gis_legs"
    dic_of_tables.update({"gis_legs":dataFrameGis_legs})
    end_time = timer()
    # dic_of_tables.append(dataFrameGis_legs)
    gis_legs= end_time - start_time

    # Waypoints
    start_time = timer()
    dataFrameWaypoints = pd.read_sql("select * from public.waypoints", dbConnection);
    dataFrameWaypoints.name = "waypoints"
    dic_of_tables.update({"waypoints":dataFrameWaypoints})
    end_time = timer()
    # dic_of_tables.append(dataFrameWaypoints)
    waypoints= end_time - start_time

    # Places
    start_time = timer()
    dataFramePlaces = pd.read_sql("select * from public.places", dbConnection);
    dataFramePlaces.name = "places"
    dic_of_tables.update({"places":dataFramePlaces})
    end_time = timer()
    # dic_of_tables.append(dataFramePlaces)
    places= end_time - start_time

    # # #using just fastest ones
    # logging.debug("The necessary time to load the data was:\n %.2f seconds for the segments \n %.2f seconds for the routes \n %.2f seconds for the gis_legs \n", segments, routes,gis_legs)
    try:
        # using all the data
        logging.debug("The necessary time to load the data was:\n %.2f seconds for the segments \n %.2f seconds for the routes \n %.2f seconds for the gis_legs \n %.2f seconds for the waypoints \n %.2f seconds for the places", segments, routes,gis_legs,waypoints, places)
        # logging.debug("The necessary time to load the data was:\n %.2f seconds for the segments \n %.2f seconds for the routes \n %.2f seconds for the gis_legs \n %.2f seconds for the waypoints \n ", segments, routes,gis_legs,waypoints)
    except NameError:
        logging.debug("The necessary time to load the data was:\n %.2f seconds for the segments \n %.2f seconds for the routes \n %.2f seconds for the gis_legs \n", segments, routes,gis_legs)



    return dic_of_tables
    # return dataFrameSegments, dataFrameRoutes, dataFrameGis_legs, waypoints


