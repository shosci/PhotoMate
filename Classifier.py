!#/bin/python

import os
import sys
import time, datetime
import exifread

file_copyed = 0

def GetDateTakenOfPhoto(filename):
	key = 'EXIF DateTimeOriginal'
	f = open(filename, 'rb')
	tags = exifread.process_file(f)
	f.close()
	try:
		t = time.strptime(str(tags[key]), '%Y:%m:%d %H:%M:%S')
		return datetime.datetime(*t[:3])
	except KeyError as arg:
		longdate = os.path.getctime(filename)
		return datetime.datetime.fromtimestamp(longdate)
	else:
		return datetime.datetime.now()
	

# according to the creat date
def TidyFile(sourcefile, targetdir):
	# if not PNG, JPG, JPEG, just skip it
	fileext = os.path.splitext(sourcefile)[1]
	if fileext.lower() != '.png' and fileext.lower() != '.jpg' and fileext.lower != '.jpeg':
		return

	basename = os.path.basename(sourcefile)
	
	datetaken = GetDateTakenOfPhoto(sourcefile)
	#print(str(date.year) + "Y" + str(date.month) + "M" + str(date.day) +"D")

	year = str(datetaken.year)
	month = '0' + str(datetaken.month) if datetaken.month < 10 else str(datetaken.month)
	day = '0' + str(datetaken.day) if datetaken.day < 10 else str(datetaken.day)

	topfolder = targetdir
	subfolder = year + '.' + month + '.' + day

	writefolder = os.path.join(topfolder, subfolder)
	#print(writefolder)

	if os.path.isfile(sourcefile):
		if not os.path.exists(writefolder):
			os.makedirs(writefolder)

		targetfile = os.path.join(writefolder, basename)

		if not os.path.exists(targetfile):
			filetowrite = open(targetfile, 'wb')
			filetoread = open(sourcefile, 'rb')
			filetowrite.write(filetoread.read())
			filetoread.close()
			filetowrite.close()
			print('file copyed - sourcefile: {0} \t targetfile: {1}'.format(sourcefile, targetfile))
			global file_copyed
			file_copyed += 1
		#os.remove(sourcefile)

def TidyDirectory(sourcedir, targetdir):
	if os.path.isdir(sourcedir):
		for item in os.listdir(sourcedir):
			#print(item)
			sourcefile = os.path.join(sourcedir, item)
			if os.path.isfile(sourcefile):
				TidyFile(sourcefile, targetdir)
			elif os.path.isdir(sourcefile):
				TidyDirectory(sourcefile, targetdir)

sourcedir = sys.argv[1]
targetdir = sys.argv[2]
TidyDirectory(sourcedir, targetdir)
print('total copyed files: ' + str(file_copyed))
