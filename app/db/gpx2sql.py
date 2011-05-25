#!/usr/bin/python

import xml.dom.minidom
from xml.dom.minidom import Node
 
import os, sys
from stat import *

import psycopg2

def db_connect():
  conn_string = "host='localhost' dbname='gpx-test' user='gpx' password='gpx' port='5433'"
  global conn
  conn = psycopg2.connect(conn_string)
  global cursor
  cursor = conn.cursor()

def db_close():
  cursor.close()
  conn.close()

def load_gpx(gps_name,filename):
  cursor.execute("SELECT * FROM gpx_files where filename = '" + filename + "' and gps_name = '" + gps_name + "';")
  if cursor.fetchone():
    return

  path = gps_name + "/Traces/" + filename
  os.system("unzip -j " + path)  
  unzipped = filename.replace(".zip","")
  
  doc = xml.dom.minidom.parse(unzipped)
  os.system("rm " + unzipped)
  
  size = str(os.stat(path)[ST_SIZE])
  trkpt = doc.getElementsByTagName("trkpt")[0]
  lat = trkpt.getAttribute("lat")
  lon = trkpt.getAttribute("lon")
  time = trkpt.getElementsByTagName("time")[0].firstChild.data

  cursor.execute("INSERT INTO gpx_files (filename,size,gps_name,geom,timestamp) values ('" + filename + "','" + size + "','" + gps_name + "'," + " Transform( ST_GeomFromText('POINT(" + lon + " " + lat + ")', 4326), 900913)" + ",'" + time + "') RETURNING id;")

  gpx_id = cursor.fetchone()[0]

  trkid = 0
  for trk in doc.getElementsByTagName("trk"):
    trkid += 1
    for trkseg in trk.getElementsByTagName("trkseg"):
      for trkpt in trkseg.getElementsByTagName("trkpt"):
        lat = trkpt.getAttribute("lat")
        lon = trkpt.getAttribute("lon")
        ele = trkpt.getElementsByTagName("ele")[0].firstChild.data
        time = trkpt.getElementsByTagName("time")[0].firstChild.data
        cursor.execute("INSERT INTO gps_points (altitude,trackid,geom,gpx_id,timestamp) values ('" + ele + "','" + str(trkid) + "'," + " Transform( ST_GeomFromText('POINT(" + lon + " " + lat + ")', 4326), 900913)" + ",'"  + str(gpx_id) + "','"  + time + "');")

  conn.commit()
  exit()
  
if __name__ == "__main__":
  db_connect()
  
  for entry in os.listdir('.'):
    if os.path.exists(entry + '/Traces/'):
      for filename in os.listdir(entry + '/Traces/'):
        if filename.find(".gpx.zip") != -1:
          load_gpx(entry, filename)  

  db_close()
