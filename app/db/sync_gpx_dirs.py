#!/usr/bin/python

#
# sync_gpx_dirs.py
# : quick script used to conlate one directory full of GPX files with another
#

import os

dest = "../../../../gps-traces-may-2011-download/"
for entry in os.listdir('.'):
  if os.path.exists(entry + '/Tracks/'):
    for filename in os.listdir(entry + '/Tracks/'):
      if filename.find(".gpx") != -1:
        filepath = entry + "/Tracks/" + filename
        destfilepath = dest + entry + "/Traces/" + filename
        os.system("zip " + filepath + ".zip " + filepath)
        if not os.path.exists(destfilepath) and not os.path.exists(destfilepath + ".zip"):
          os.system("cp " + filepath + ".zip " + destfilepath + ".zip")
