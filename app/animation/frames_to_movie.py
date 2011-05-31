#!/usr/bin/python

#For each image sorted by date
#  Combine with previous image into background image
#    composite in1.png background.png background-new.png
#  Make background image with increased transparency
#    convert /tmp/out.png -alpha on -channel a -evaluate set 75% /tmp/out2.png  
#  Comine with increased transparency background image into iterated 
#    composite in1.png in2.png out.png
#  
#  To add a halo
#    convert -channel RGBA -blur 5x8 2010-08-16T14\:00\:00.png blur.png
#    convert -fill white +opaque black blur.png white.png
#    composite 2010-08-16T14\:00\:00.png white.png halo.png
#
#Then
#  ffmpeg -qscale 5 -r 10 -i frame-%04d.jpg movie.mp4
  
import os
import subprocess
     
i = 1     
blanks = 0
inpath = 'frames/'
path = 'out/'

z = 3
imgx = 336 * z
imgy = 450 * z
    
background = path + "background.png"
backgroundtmp = path + "background-tmp.png"
blur = path + "blur.png"
white = path + "white.png"
halo = path + "halo.png"
label = path + "label.png"

dirList=os.listdir(inpath)
dirList.sort()
for fname in dirList:
  imgpath = inpath + fname

  # If current frame is blank, and we've already added X blank frames, skip
  if (float(subprocess.check_output(["identify", "-format", "%[standard-deviation]", imgpath])) == 0):
    blanks += 1
    if blanks > 4:
      continue

  newframe = path + "frame-{0:04d}.jpg".format(i)
  i += 1
  
  # Add current frame to background  
  if not os.path.exists(background):
    os.system("cp " + imgpath + " " + background)
  else:
    os.system("composite " + imgpath + " " + background + " " + backgroundtmp)
    os.system("mv " + backgroundtmp + " " + background)
    
  # Increase transparency on background  
  os.system("convert " + background + " -alpha on -channel a -evaluate set 75% " + backgroundtmp)   

  # Create halo
  os.system("convert -channel RGBA -blur 5x8 " + imgpath + " " + blur)
  os.system("convert -fill white +opaque black " + blur + " " + white)
  os.system("composite " + imgpath + " " + white + " " + halo)

  os.system("composite " + halo + " " + backgroundtmp + " " + newframe)
  
  #os.system("convert 200x320.tif -bordercolor white -border 200x160 -gravity center -crop 400x320+0+0 400x320.tif")

  # Add Label
  labeltext = fname.partition("T")[0] + '\n' + 'MICS Swaziland'
  os.system("convert -background transparent -fill white -size " + str(imgx) + "x" + str(imgy)+ " -gravity SouthWest -font Palatino-Roman -pointsize 36 label:'" + labeltext + "' " + label)

  os.system("composite " + label + " " + newframe + " " + newframe)
