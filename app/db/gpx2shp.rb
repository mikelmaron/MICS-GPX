#!/usr/bin/ruby

require 'rubygems'
require 'geo_ruby'
include GeoRuby::Shp4r

DIR = ARGV[0]
Shape = ARGV[1]

i = 1
lat = nil
lon = nil
time = nil

shapefile = ShpFile.create(DIR + Shape,ShpType::POINT,[Dbf::Field.new("date","C",10),Dbf::Field.new("id","N",10,0)])

Dir.entries( DIR ).sort.each { | file |
  if ! File.directory?(DIR + file) and file.index(".gpx") 
    File.open(DIR+file, 'r') do |infile|
      while (line = infile.gets)
        scan = line.scan(/\<trkpt lat\=\"(.*?)\" lon=\"(.*?)\"\>/)
        if scan.size > 0
          lat = scan[0][0]
          lon = scan[0][1]
        end
        scan = line.scan(/\<time\>(.*?)\<\/time\>/)
        if scan.size > 0
          time = scan[0][0]
        end
        scan = line.scan(/<\/trkpt>/)
        if scan.size > 0
          if ! lat.nil? and ! lon.nil? and ! time.nil?
            shapefile.transaction do |tr|
                tr.add(ShpRecord.new(ShpType::POINT.from_x_y(lon,lat),'date' => time,'id' => i))
            end    
            #print i.to_s + "," + lat.to_s + "," + lon.to_s + "," + time.to_s + "\n"
            i = i + 1
          end
          lat = nil
          lon = nil
          time = nil
        end     
      end
    end  
  end
}

shpfile.close
