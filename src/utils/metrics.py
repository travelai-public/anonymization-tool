# This Python file uses the following encoding: utf-8
import sys, os, logging, csv, coloredlogs, colorlog
import psycopg2
from itertools import *
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from timeit import default_timer as default_timer
import math

import seaborn as sn
import matplotlib.pyplot as plt

import geopandas as gpd
import contextily as ctx

import shapely
from shapely.geometry import LineString


## Ref from https://datatofish.com/correlation-matrix-pandas/



## calculates the correlation of a table/dataframe
def correlation(data_frame):

    return data_frame.corr()

## generates new dic with correlaiton matrices
def correlation_of_all_dataframes(dic_of_tables):
    
    correlated_dic_of_tables ={}
    # print(correlation(dic_of_tables["segments"]))
    correlated_dic_of_tables.update({"segments": correlation(dic_of_tables["segments"])})
    # print(correlation(dic_of_tables["routes"]))
    correlated_dic_of_tables.update({"routes": correlation(dic_of_tables["routes"])})
    # print(correlation(dic_of_tables["gis_legs"]))
    correlated_dic_of_tables.update({"gis_legs": correlation(dic_of_tables["gis_legs"])})
    if "waypoints" in dic_of_tables:
        # print(correlation(dic_of_tables["waypoints"]))
        correlated_dic_of_tables.update({"waypoints": correlation(dic_of_tables["waypoints"])})

    return correlated_dic_of_tables

def show_graphics(dic_of_tables):

    print(dic_of_tables)

    for key,value in dic_of_tables.items():
        logging.debug('Drawing %s heatmap...',key)
        sn.heatmap(value, annot=True)

        plt.show()



def retrive_min_max_values(column):

    # print(column)

    return column.min(), column.max()



    # for key,value in dic_of_tables.items():
    #     if key == "gis_legs":
    #         print("Key:", key)
    #         print("Value:", value)
    #         print("Value(type):", type(value))

    #         print(value["first_location"])
    #         print(value["last_location"])
    #         input()

    #         print(value["first_location"][57590])
    #         print(value["last_location"][57590])
    #         input()
    #         #print(type(value["first_location"][57590]))

    #         #print("first location(type):", type(value["first_location"]))
    #         #print(value["last_location"])
    #         # print(value["routes_count"].max())
    #         # print(value["routes_count"].min())

    #         # coord = hex_to_coord(value["first_location"][57590])

    #         # print("X: ",coord.x)
    #         # print("New X: ",coord.x +5.600)
    #         # print("Y: ",coord.y)
    #         # print("New Y: ",coord.y + 5.789524)
    #         # print("Area: ",coord.area)
    #         # print("Length: ",coord.length)
    #         # print("Bounds: ",coord.bounds)

    #         # coord_to_hex(coord)
    #         # input()

    #         # line = LineString([(3, 3), (1, 1)])
    #         # print("Line area: ",line.area)
    #         # print("Line length: ",line.length)
    #         # # print(coord_length([0,0],[1,1]))
    #         # print(coord_length(coord,[1,1]))
    #         # print("Distance in KM: ", calc_distance([1,1.15000],[1,1.15500]))




    #     if key == "waypoints":
    #         print("Key:", key)
    #         print("Value:", value)
    #         #print("Value(type):", type(value))
    #         print(value["location"])
    #         print(value["location"][0])

    




def hex_to_coord(hex_string):
    ## Input is a string

    ## geom = shapely.wkb.loads(value["first_location"][57590], hex=True)
    ## geom = shapely.wkb.loads(hex_string, hex=True)

    ## returns a shapely.geometry.point.Point (latitude and longitude)

    return shapely.wkb.loads(hex_string, hex=True)

def coord_to_hex(coord):

    ## input is a a shapely.geometry.point.Point (latitude and longitude)

    ## coord.wkb_hex
    ## print(geom.wkb_hex)

    ## returns a string

    return coord.wkb_hex

def coord_length(coord1, coord2):
    ## input is:  shapely_point,shapely_point
    ## or 
    ## numerical input such as: [1,50],[1,50] or [0,547,0,658],[1,665,1,657]
    line = LineString([coord1, coord2])

    return line.length


def calc_distance(coord1, coord2):

    ## Distance is returned in KM's

    ## input is:  shapely_point,shapely_point
    ## or 
    ## numerical input such as: [1,50],[1,50] or [0,547,0,658],[1,665,1,657]


    ## Radius of earth 6371
    
    try:
        distance = math.acos(math.sin(math.radians(coord1.y))*math.sin(math.radians(coord2.y))+math.cos(math.radians(coord1.y))*math.cos(math.radians(coord2.y))*math.cos(math.radians(coord2.x)-math.radians(coord1.x)))*6371
    except AttributeError as e:
        distance = math.acos(math.sin(math.radians(coord1[1]))*math.sin(math.radians(coord2[1]))+math.cos(math.radians(coord1[1]))*math.cos(math.radians(coord2[1]))*math.cos(math.radians(coord2[0])-math.radians(coord1[0])))*6371
    return distance













