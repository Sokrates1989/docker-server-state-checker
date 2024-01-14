## Date based string functions like getting string of current day for logfiles.

# Get date.
from datetime import datetime
# For getting unixtimestamp.
import time

# Get string like "2022_03_31".
def getDateStringForLogFileName():
	now  = datetime.now()
	return now.strftime("%Y_%m_%d")

# Get string like "[2022-03-31 22:02:04]".
def getDateStringForLogTag():
	now  = datetime.now()
	date_time = now.strftime("%Y-%m-%d %H:%M:%S")
	currentLogTimeString = "[" + date_time + "]"
	return currentLogTimeString


# Convert creation date string received from google drive to unix timestamp.
# Google drive creation date string loks like this 2022-07-06T08:00:37.685Z.
def convertGoogleDriveDateStringToUnixTimeStamp(googleDriveDateString):
	datePart = getDatePartFromGoogleDriveDateString(googleDriveDateString)
	timePart = getTimePartFromGoogleDriveDateString(googleDriveDateString)
	unixTimestamp = datetime.now()
	unixTimestamp = unixTimestamp.replace(year=getYearFromGoogleDriveDatePart(datePart))
	unixTimestamp = unixTimestamp.replace(month=getMonthFromGoogleDriveDatePart(datePart))
	unixTimestamp = unixTimestamp.replace(day=getDayFromGoogleDriveDatePart(datePart))
	unixTimestamp = unixTimestamp.replace(hour=getHourFromGoogleDriveTimePart(timePart))
	unixTimestamp = unixTimestamp.replace(minute=getMinuteFromGoogleDriveTimePart(timePart))
	unixTimestamp = unixTimestamp.replace(second=getSecondFromGoogleDriveTimePart(timePart))
	return int(time.mktime(unixTimestamp.timetuple()))


# Get date part from googleDrive datestring.
# 2022-07-06 from 2022-07-06T08:00:37.685Z.
def getDatePartFromGoogleDriveDateString(googleDriveDateString):
	return googleDriveDateString[0:googleDriveDateString.find('T')]

# Get year from date part.
# 2022 from 2022-07-06.
def getYearFromGoogleDriveDatePart(datePart):
	return int(str(datePart).split("-")[0])

# Get month from date part.
# 7 from 2022-07-06.
def getMonthFromGoogleDriveDatePart(datePart):
	return int(str(datePart).split("-")[1])

# Get day from date part.
# 6 from 2022-07-06.
def getDayFromGoogleDriveDatePart(datePart):
	return int(str(datePart).split("-")[2])



# Get time part from googleDrive datestring.
# 08:00:37 from 2022-07-06T08:00:37.685Z.
def getTimePartFromGoogleDriveDateString(googleDriveDateString):
	return googleDriveDateString[googleDriveDateString.find('T')+1:googleDriveDateString.find('.')]

# Get hour from date part.
# 8 from 08:00:37.
def getHourFromGoogleDriveTimePart(timePart):
	return int(str(timePart).split(":")[0])

# Get month from date part.
# 0 from 08:00:37.
def getMinuteFromGoogleDriveTimePart(timePart):
	return int(str(timePart).split(":")[1])

# Get day from date part.
# 37 from 08:00:37.
def getSecondFromGoogleDriveTimePart(timePart):
	return int(str(timePart).split(":")[2])