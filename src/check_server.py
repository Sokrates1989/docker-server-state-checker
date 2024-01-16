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
import serverReportUtils as ServerReportUtils
# Sending report Utils.
import sendReportUtils

## Initialize vars.

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
    serverReportUtils = ServerReportUtils.ServerReportUtils()
    serverReport = serverReportUtils.getServerReport()

    # Log information.
    logger.logInformation(serverReport.getServerReportMessage())

    # Send message to admin telegram chat.
    sendReportUtils.sendServerReport(serverReport)



# Send the current state of the server to channels.
try:
    handleServerReport()
except Exception as e:
    # If there is an error handling the server report, try to send info about that as well.
    handleCommandException("handleServerReport", e)
