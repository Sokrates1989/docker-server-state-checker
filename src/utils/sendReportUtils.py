## Utilities for report or info message creation.

# For getting current timestamp.
import time
# For file operations with operating system.
import os
# For getting config.
import json
# To create enumerations.
from enum import Enum

## Own classes.
from serverReport import ServerReport
from serverReport import MostCrucialServerState
import telegramUtils
import fileUtils
import timeStringUtils

class MessagingPlatform(Enum):
    DEFAULT = "Default"
    EMAIL = "Email"
    TELEGRAM = "Telegram"

# Config file.
config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config/", "config.txt")
config_file = open(config_file_pathAndName)
config_array = json.load(config_file)

# Path to serverInfo and last sent files.
serverInfoPath = os.path.join(os.path.dirname(__file__), "..", "..", "serverInfo/")
lastSentInfoFile = serverInfoPath + "lastSentInfoReport.txt"
lastSentWarningFile = serverInfoPath + "lastSentWarningReport.txt"
lastSentErrorFile = serverInfoPath + "lastSentErrorReport.txt"

# Message frequency.
maxInfoReportFrequencySeconds = config_array['messageFrequency']['info'].strip().strip("\"")
maxWarningReportFrequencySeconds = config_array['messageFrequency']['warning'].strip().strip("\"")
maxErrorReportFrequencySeconds = config_array['messageFrequency']['error'].strip().strip("\"")
maxInfoReportFrequencySeconds = timeStringUtils.convert_time_string_to_seconds(maxInfoReportFrequencySeconds)
maxWarningReportFrequencySeconds = timeStringUtils.convert_time_string_to_seconds(maxWarningReportFrequencySeconds)
maxErrorReportFrequencySeconds = timeStringUtils.convert_time_string_to_seconds(maxErrorReportFrequencySeconds)


# Send server report based on state and last sent report date.
def sendServerReport(serverReport: ServerReport, messagePlatform: MessagingPlatform = MessagingPlatform.DEFAULT):
    if shouldInfoReportBeSent():
        sendInfoReport(serverReport.getServerReportMessage())
    
    if shouldWarningReportBeSent(serverReport.getMostCrucialState()):
        sendWarningReport(serverReport.getServerReportMessage())
    
    if shouldErrorReportBeSent(serverReport.getMostCrucialState()):
        sendErrorReport(serverReport.getServerReportMessage())
    


# Should the info report be sent.
def shouldInfoReportBeSent():
    lastSentInfoUnixTimestamp = getLastSentUnixTimestamp(lastSentInfoFile)
    if lastSentInfoUnixTimestamp + maxInfoReportFrequencySeconds < int(time.time()):
        return True
    else:
        return False


# Send info report and write last sent state to file.
def sendInfoReport(reportMessage):

    # Send Info Report Message.
    telegramUtils.sendInfoMessage(reportMessage)

    # Write to file when the last Info report message has been sent.
    fileUtils.overwriteContentOfFile(lastSentInfoFile, time.time())


    
# Should the warning report be sent.
def shouldWarningReportBeSent(mostCrucialServerState: MostCrucialServerState):

    # Is most crucial server state at least warning?
    if mostCrucialServerState == MostCrucialServerState.WARNING or mostCrucialServerState == MostCrucialServerState.ERROR:
        # Are frequency limits reached.
        lastSentWarningUnixTimestamp = getLastSentUnixTimestamp(lastSentWarningFile)
        if lastSentWarningUnixTimestamp + maxWarningReportFrequencySeconds < int(time.time()):
            return True
        else:
            return False
    else:
        return False

# Send warning report and write last sent state to file.
def sendWarningReport(reportMessage):
    
    # Send Warning Report Message.
    telegramUtils.sendWarningMessage(reportMessage)

    # Write to file when the last Warning report message has been sent.
    fileUtils.overwriteContentOfFile(lastSentWarningFile, time.time())


    
# Should the error report be sent.
def shouldErrorReportBeSent(mostCrucialServerState: MostCrucialServerState):
    # Is most crucial server state Error?
    if mostCrucialServerState == MostCrucialServerState.ERROR:
        # Are frequency limits reached.
        lastSentErrorUnixTimestamp = getLastSentUnixTimestamp(lastSentErrorFile)
        if lastSentErrorUnixTimestamp + maxErrorReportFrequencySeconds < int(time.time()):
            return True
        else:
            return False
    else:
        return False
    
# Send error report and write last sent state to file.
def sendErrorReport(reportMessage):
    
    # Send Error Report Message.
    telegramUtils.sendErrorMessage(reportMessage)

    # Write to file when the last error report message has been sent.
    fileUtils.overwriteContentOfFile(lastSentErrorFile, time.time())


# Get last sent time.
def getLastSentUnixTimestamp(fileToGetTimeStampOf) -> int:
    try:
        content = fileUtils.readStringFromFile(fileToGetTimeStampOf)
        float_value = float(content)
        return int(float_value)
    except Exception as e:
        print(f"getLastSentUnixTimestamp File does not exist or could not be converted to valid unixtimestamp, returning 0: {e}")
        return 0
