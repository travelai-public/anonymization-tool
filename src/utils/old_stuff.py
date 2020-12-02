# This Python file uses the following encoding: utf-8
import sys, os, logging, csv, coloredlogs
import psycopg2
from itertools import *
import pandas as pds
from sqlalchemy import create_engine

#to write debug messages on screen
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


#to write debug messages to file
#logging.basicConfig(filename='debug.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':

    # not necessary for now..
    #coloredlogs.install()

    logging.debug('Initializing...')


    ## DB Connection

    ## I changed the DB port due to installation issues. 
    ## Now it is 5433
    #conn = psycopg2.connect(database="travelai", user = "paulosilva", password = "", host = "127.0.0.1", port = "5433")

    conn = psycopg2.connect(database="tp2", user = "paulosilva", password = "", host = "127.0.0.1", port = "5433")

    print("Opened database successfully")
    print(conn)


    cur = conn.cursor()

    ## Get Segments

    cur.execute("SELECT id, installation_id,start_ts, end_ts, meta, uploadtime, routes_count, legs_count, gaps_count, obsolete, overwrites, overwritten_by, start_place_id, end_place_id, gislegs_count from public.segments")
    rows = cur.fetchall()
    for row in rows:
       print("ID = ", row[0], "\n")
       print("installation_id = ", row[1], "\n")
       print("start_ts = ", row[2], "\n")
       print("end_ts = ", row[3], "\n")
       print("distance = ", row[4], "\n")
       print("GIS_DISTANCE = ", row[5], "\n")
       print("duration = ", row[6], "\n")
       print(row)

    print("Operation public.segments...")

    input()

    ## Get Routes

    cur.execute("SELECT id,installation_id,start_ts,end_ts,distance,gis_distance,duration,start_place,end_place,start_dwell,end_dwell,data_quality,match_confidence,meta,uploadtime,segment_id,obsolete,overwritten_by,overwrites from public.routes")
    rows = cur.fetchall()
    for row in rows:
       print("ID = ", row[0], "\n")
       print("installation_id = ", row[1], "\n")
       print("start_ts = ", row[2], "\n")
       print("end_ts = ", row[3], "\n")
       print("distance = ", row[4], "\n")
       print("GIS_DISTANCE = ", row[5], "\n")
       print("duration = ", row[6], "\n")
       print(row)
       

    print("Operation public.routes...")
    
    input()

    cur.execute("Select * FROM public.routes LIMIT 0")
    colnames = [desc[0] for desc in cur.description]
    print(colnames)

    input()

    ## Get GISLegs

    # cur.execute("SELECT id,installation_id,start_ts,end_ts,distance,gis_distance,duration,start_place,end_place,start_dwell,end_dwell,data_quality,match_confidence,meta,uploadtime,segment_id,obsolete,overwritten_by,overwrites from public.routes")
    # rows = cur.fetchall()
    # for row in rows:
    #    print("ID = ", row[0], "\n")
    #    print("installation_id = ", row[1], "\n")
    #    print("start_ts = ", row[2], "\n")
    #    print("end_ts = ", row[3], "\n")
    #    print("distance = ", row[4], "\n")
    #    print("GIS_DISTANCE = ", row[5], "\n")
    #    print("duration = ", row[6], "\n")
    #    print(row)


    cur.execute("SELECT * from public.gis_legs")
    rows = cur.fetchall()
    for row in rows:
       print("ID = ", row[0], "\n")
       print("ID = ", row[0], "\n")

    print("Operation public.GISLegs...")

    input()

    conn.close()

    logging.debug('Closing...')




    

