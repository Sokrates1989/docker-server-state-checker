## Execute this file to test if tools are up and running.

# To create timestamp.
import time
# To get config json.
import json
# Be able to write trace to logfile.
import traceback

# Import own classes.
# Insert path to utils to allow importing them.
import os
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "utils"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "models"))

import logger as Logger
# To interact with telegramBots.
import telegramUtils
# Get SeverStateReport.
import serverReportUtils
# Sending report Utils.
import sendReportUtils

## Initialize vars.

# Get config.
config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "config/", "config.txt")
config_file = open(config_file_pathAndName)
config_array = json.load(config_file)

# Instantiate classes.
# Logger.
logger = Logger.Logger("check_tools")


# Handles error exceptions (log and info to admin).
def handleCommandException(exceptionLocationAndAdditionalInformation, exception):
    # Log error.
    errorLogText = exceptionLocationAndAdditionalInformation + " " + str(exception)
    # Add traceback to logfile.
    traceOfError = traceback.format_exc()
    logger.logError(str(traceOfError) + "\n" + errorLogText)

    # Send warning message via telgram.
    telegramUtils.sendWarningMessage(errorLogText)


# Handle server report (get server state, check thresholds and send messages).
def handleServerReport():

    # Get the server report.
    serverReport = serverReportUtils.getServerReport()

    # Log information.
    logger.logInformation(serverReport.getServerReportMessage())

    # Send message to admin telegram chat.
    sendReportUtils.sendServerReport(serverReport)



# Send the current state of the server to channels.
handleServerReport()
