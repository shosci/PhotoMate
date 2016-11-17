#!/bin/python

import os
import sys
import time, datetime
import exifread
from geopy.geocoders import Nominatim
import random

file_copyed = 0

file_skipped = 0

class Logger:
    def __init__(self, directory):
        self.log_file = os.path.join(directory, 'log.txt')
        self.log_stream = open(self.log_file, 'w')

    def info(self, info_str):
        self.log_stream.write('info: ' + info_str + os.linesep)

    def warn(self, warn_str):
        self.log_stream.write('warning: ' + warn_str + os.linesep)

    def error(self, error_str):
        self.log_stream.write('error: ' + error_str + os.linesep)

    def finalize(self)
        self.log_stream.flush()
        self.log_stream.close()

# returns a tuple ([Country, State, Region], [Year, Month, Day])
def GetLocationAndDateOfPhoto(filename):
        tags = GetExifTags(filename)

        # Get location
        location_lat_ref_key = 'GPS GPSLatitudeRef'
        location_lat_key = 'GPS GPSLatitude'
        location_lon_ref_key = 'GPS GPSLongitudeRef'
        location_lon_key = 'GPS GPSLongitude'

	location = []
	if tags.has_key(location_lat_ref_key):
        	geodegrees = GetGeoDecimalDegrees(tags[location_lat_ref_key], \
        	        tags[location_lat_key], tags[location_lon_ref_key], \
        	        tags[location_lon_key])
		#for key in tags.keys():
		#	if key[:3] == 'GPS':
		#		print('Key: {0}, Value: {1}'.format(key, tags[key]))
		try:
        		geolocator = Nominatim()
        		geo_location = geolocator.reverse(geodegrees)
        		geo_address = geo_location.raw['address']
        		country = geo_address['country']
        		state = geo_address['state']
			region = 'unknown'
			if geo_address.has_key('region'):
        			region = geo_address['region'].split('/')[0].strip()
			elif geo_address.has_key('county'):
				region = geo_address['county'].split('/')[0].strip()
        		#location = [country, state]
        		location = [country, state, region]
		except KeyError as arg:
			print(geo_address)
	else:
		print('file {0} has no geo info'.format(filename))

        # Get date
	date_key = 'EXIF DateTimeOriginal'
	try:
		t = time.strptime(str(tags[date_key]), '%Y:%m:%d %H:%M:%S')
		t = datetime.datetime(*t[:3])
	except KeyError as arg:
                # fall back to creation time
		longdate = os.path.getctime(filename)
		t = datetime.datetime.fromtimestamp(longdate)
	else:
		t = datetime.datetime.now()
	year = str(t.year)
	month = '0' + str(t.month) if t.month < 10 else str(t.month)
	day = '0' + str(t.day) if t.day < 10 else str(t.day)
        date = [year, month, day]
        return (location, date)

def GetExifTags(filename):
	f = open(filename, 'rb')
	tags = exifread.process_file(f)
	f.close()
        return tags

def GetGeoDecimalDegrees(lat_ref, lat, lon_ref, lon):
        lat_dms = GetDmsFormat(lat)
        lat = lat_dms[0] + lat_dms[1]/60.0 + (lat_dms[2]/60.0)/60.0
        if lat_ref == 'S':
            lat = -lat

        lon_dms = GetDmsFormat(lon)
        lon = lon_dms[0] + lon_dms[1]/60.0 + (lon_dms[2]/60.0)/60.0
        if lon_ref == 'W':
            lon = -lon
        return str(lat) + ', ' + str(lon)
    
def GetDmsFormat(lat_or_lon_instanceOfIfdTag):
        l_str = str(lat_or_lon_instanceOfIfdTag)
        l_str = l_str.strip('[').strip(']')
        l_dms = l_str.split(',')
        l_dms = list(map(lambda item: item.strip(), l_dms))
        assert(len(l_dms) == 3)
        l_d = int(l_dms[0])
        l_m = int(l_dms[1])
        l_s_molecular_form = l_dms[2].split('/')
        l_s = float(l_s_molecular_form[0])/float(l_s_molecular_form[1])
        return [l_d, l_m, l_s]
	
def rename(filename):
	(path, ext) = os.path.splitext(filename)
	randomint = random.randint(0,100)
	return path + str(randomint) + ext

# according to the location where the photo was taken and then the creation date
# in format of yyyy-MM-dd
def TidyFile(sourcefile, targetdir):
	# if not PNG, JPG, JPEG, just skip it
	fileext = os.path.splitext(sourcefile)[1]
	if fileext.lower() != '.png' and fileext.lower() != '.jpg' and fileext.lower != '.jpeg':
                # printing a log
                file_skipped += 1
		return

	basename = os.path.basename(sourcefile)
	
	(location, date) = GetLocationAndDateOfPhoto(sourcefile)
	# Output file path
	# Country/State/Region/Year-Month-Day/
	inter_folders = list(location)
	inter_folders.append('-'.join(date))

	outputfolder = os.path.join(targetdir, *inter_folders)

	if os.path.isfile(sourcefile):
		if not os.path.exists(outputfolder):
			os.makedirs(outputfolder)

		targetfile = os.path.join(outputfolder, basename)
		# in case there are different files having the same name
		while os.path.exists(targetfile):
			targetfile = rename(targetfile)	

		if not os.path.exists(targetfile):
			filetowrite = open(targetfile, 'wb')
			filetoread = open(sourcefile, 'rb')
			filetowrite.write(filetoread.read())
			filetoread.close()
			filetowrite.close()
			print('file copyed - sourcefile: {0} \t targetfile: {1}'.format(sourcefile, targetfile.encode('utf-8')))
			global file_copyed
			file_copyed += 1
		#os.remove(sourcefile)

def TidyDirectory(sourcedir, targetdir):
	if os.path.isdir(sourcedir):
		for item in os.listdir(sourcedir):
			sourcefile = os.path.join(sourcedir, item)
			if os.path.isfile(sourcefile):
				TidyFile(sourcefile, targetdir)
			elif os.path.isdir(sourcefile):
				TidyDirectory(sourcefile, targetdir)
if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: Classifier.py SourceDir OutputDir')
		exit(0)
	sourcedir = sys.argv[1]
	targetdir = sys.argv[2]

	TidyDirectory(sourcedir, targetdir)
	print('File skipped: ' + str(file_skipped))
	print('File copied: ' + str(file_copyed))
