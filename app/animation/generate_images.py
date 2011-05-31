#!/usr/bin/python

import mapnik2 as mapnik
from mapnik2 import Layer, PostGIS
from datetime import datetime, timedelta
import sys, os

def render_image(start_time,end_time):
    
    ll = (30.708,-27.414,32.179,-25.652)
    prj = mapnik.Projection("+init=epsg:900913")
    c0 = prj.forward(mapnik.Coord(ll[0],ll[1]))
    c1 = prj.forward(mapnik.Coord(ll[2],ll[3]))

    z = 3
    imgx = 336 * z
    imgy = 450 * z

    m = mapnik.Map(imgx,imgy)
    mapnik.load_map(m,"gpx-nolayer.xml")
    
    db_params = dict(
      dbname = 'gpx-merc',
      user = 'gpx',
      password = 'gpx',
      host = 'localhost',
      port = 5433,
      estimate_extent = False,
      extent = "3390650.221286806, -3163145.87245787, 3609898.596229789, -2956043.104540316"
    )

    lyr = Layer('points',"+init=epsg:900913")
    db_params['table'] = '(select gps_points.geom as geom, gpx_files.gps_name as gps_name from gps_points INNER join gpx_files on gpx_files.id = gps_points.gpx_id where gps_points.timestamp >= \'' + start_time + '\' and gps_points.timestamp < \'' + end_time + '\') as points'
    lyr.datasource = PostGIS(**db_params)
    lyr.styles.append('points')
    m.layers.append(lyr)
    
    if hasattr(mapnik,'mapnik_version') and mapnik.mapnik_version() >= 800:
        bbox = mapnik.Box2d(c0.x,c0.y,c1.x,c1.y)
    else:
        bbox = mapnik.Envelope(c0.x,c0.y,c1.x,c1.y)
    m.zoom_to_box(bbox)
    im = mapnik.Image(imgx,imgy)
    mapnik.render(m, im)
    view = im.view(0,0,imgx,imgy) # x,y,width,height
    view.save("frames/" + start_time + ".png",'png')
    

if __name__ == "__main__":
  cur_time = datetime(2010,8,10,0,0,0)
  end_time = datetime(2010,12,6,23,59,59)
  delta = timedelta(minutes=+30)
  while cur_time < end_time:
    render_image(cur_time.isoformat(), (cur_time+delta).isoformat())
    cur_time = cur_time + delta
