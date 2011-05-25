#!/usr/bin/python

#
# get_osm_gpx.py
# : downloads all GPX files uploaded to OSM for group of users
#

import urllib2
import re
from BeautifulSoup import BeautifulSoup
import os

for num in range(1,9):
  osm_user = 'gps0' + str(num) + 'swazisurvey'
  
  f = re.compile("/user/" + osm_user + "/traces/(\d+)")
  for page in range(1,4):
    url = 'http://www.openstreetmap.org/user/' + osm_user + '/traces/page/' + str(page)
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    anchors = soup.findAll(href=f)
    for a in anchors:
      contents = str(a.contents[0])
      if contents[0].isdigit():
        gpx_num = f.search(str(a)).group(1)
        os.system("wget http://www.openstreetmap.org/trace/" + gpx_num + "/data -O GPS_" + str(num) + "/Traces/" + contents)

      
#  for gpx_id in s:
#    url = 'http://www.openstreetmap.org/trace/' + gpx_id + '/data'
