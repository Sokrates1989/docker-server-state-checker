## Utilities for report or info message creation.

# For getting current timestamp.
import time
# For file operations with operating system.
import os
# To improve error indication (sys.exit).
import sys
# For getting config.
import json
# To create enumerations.
from enum import Enum

## Own classes.
from serverReport import ServerReport
import timeStringUtils

class MessagingPlatform(Enum):
    DEFAULT = "Default"
    EMAIL = "Email"
    TELEGRAM = "Telegram"

# Config file.
config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config/", "config.txt")
config_file = open(config_file_pathAndName)
config_array = json.load(config_file)

# ServerInfoFile.
try:
    serverInfo_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "serverInfo/", "system_info.json")
    serverInfo_file = open(serverInfo_file_pathAndName)
    serverInfo_array = json.load(serverInfo_file)
except Exception as e:
    print(f"\ncould not read serverInfo/system_info.json: {e} \nDid you map the serverInfo directory correctly? \nHas the report been created on the server? \n")
    sys.exit(1)  # Use a non-zero exit code to indicate an error


# ServerName.
serverName = os.getenv('serverName') or config_array.get('serverName') or "Unknown - Please set serverName in Env or config"
serverName = serverName.strip().strip('"')

# Create a simple consize text message from the server state json and server state.
def getServerReport(messagePlatform: MessagingPlatform = MessagingPlatform.DEFAULT) -> ServerReport:

    # Save, if there have been warnings or errors.
    hasWarning=False
    hasError=False

    # Icons to emphasize warning or error state.
    errorIcon="🚨"
    warningIcon="⚠️"
    
    # Helper function to format text as preformatted.
    def preformatted(text):
        return f"<code>{text}</code>"

    # Initialize the serverReport.
    serverReport = ""

    # Hostname.
    serverReport += f"<b>Hostname:</b> {preformatted(serverInfo_array['system_info']['hostname'])}\n"

    # Timestamp.
    current_timestamp = int(time.time())
    system_info_timestamp = serverInfo_array['timestamp']['unix_format']
    thresholds = get_thresholds('timestampAgeMinutes')
    stateIndicatingIcon = ""
    if int(current_timestamp) > int(system_info_timestamp) + float(thresholds.error) * 60:
        hasError = True
        stateIndicatingIcon = errorIcon
    elif int(current_timestamp) > int(system_info_timestamp) + float(thresholds.warning) * 60:
        hasWarning = True
        stateIndicatingIcon = warningIcon
    serverReport += stateIndicatingIcon + f"<b>Timestamp:</b> {preformatted(serverInfo_array['timestamp']['human_readable_format'])}\n"

    # Add Last 15min CPU Percentage.
    thresholds = get_thresholds('cpu')
    stateIndicatingIcon = ""
    system_value = float(serverInfo_array['cpu']['last_15min_cpu_percentage'].strip().strip("%"))
    if system_value > float(thresholds.error):
        hasError = True
        stateIndicatingIcon = errorIcon
    elif system_value > float(thresholds.warning):
        hasWarning = True
        stateIndicatingIcon = warningIcon
    cpu_percentage_string=serverInfo_array['cpu']['last_15min_cpu_percentage'] + "%"
    serverReport += stateIndicatingIcon + f"<b>CPU:</b> {preformatted(cpu_percentage_string)}\n"

    # Add Disk Usage information.
    thresholds = get_thresholds('disk')
    stateIndicatingIcon = ""
    system_value = float(serverInfo_array['disk']['disk_usage_percentage'].strip().strip("%"))
    if system_value > float(thresholds.error):
        hasError = True
        stateIndicatingIcon = errorIcon
    elif system_value > float(thresholds.warning):
        hasWarning = True
        stateIndicatingIcon = warningIcon
    disk_usage_info = f"{serverInfo_array['disk']['disk_usage_percentage']} " \
                      f"({serverInfo_array['disk']['disk_usage_amount']} / {serverInfo_array['disk']['total_disk_avail']})"
    serverReport += stateIndicatingIcon + f"<b>Disk:</b> {preformatted(disk_usage_info)}\n"

    # Add Memory Usage information.
    thresholds = get_thresholds('memory')
    stateIndicatingIcon = ""
    system_value = float(serverInfo_array['memory']['memory_usage_percentage'].strip().strip("%"))
    if system_value > float(thresholds.error):
        hasError = True
        stateIndicatingIcon = errorIcon
    elif system_value > float(thresholds.warning):
        hasWarning = True
        stateIndicatingIcon = warningIcon
    memory_usage_info = f"{serverInfo_array['memory']['memory_usage_percentage']}% " \
                        f"({serverInfo_array['memory']['used_memory_human']} / {serverInfo_array['memory']['total_memory_human']})"
    serverReport += stateIndicatingIcon + f"<b>Memory:</b> {preformatted(memory_usage_info)}\n"

    # Add Swap Status information.
    stateIndicatingIcon = ""
    if serverInfo_array['swap']['swap_status'] != "Off":
        hasWarning = True
        stateIndicatingIcon = warningIcon
    serverReport += stateIndicatingIcon + f"<b>Swap Status:</b> {preformatted(serverInfo_array['swap']['swap_status'])}\n"

    # Add Processes.
    thresholds = get_thresholds('processes')
    stateIndicatingIcon = ""
    system_value = float(serverInfo_array['processes']['amount_processes'])
    if system_value > float(thresholds.error):
        hasError = True
        stateIndicatingIcon = errorIcon
    elif system_value > float(thresholds.warning):
        hasWarning = True
        stateIndicatingIcon = warningIcon
    serverReport += stateIndicatingIcon + f"<b>Processes:</b> {preformatted(serverInfo_array['processes']['amount_processes'])}\n"
    
    # Users information.
    thresholds = get_thresholds('users')
    stateIndicatingIcon = ""
    system_value = float(serverInfo_array['users']['logged_in_users'])
    if system_value > float(thresholds.error):
        hasError = True
        stateIndicatingIcon = errorIcon
    elif system_value > float(thresholds.warning):
        hasWarning = True
        stateIndicatingIcon = warningIcon
    serverReport += stateIndicatingIcon + f"<b>Logged In Users:</b> {preformatted(serverInfo_array['users']['logged_in_users'])}\n"

    # Add Updates information.
    thresholds = get_thresholds('updates')
    stateIndicatingIcon = ""
    system_value = float(serverInfo_array['updates']['amount_of_available_updates'])
    if system_value > float(thresholds.error):
        hasError = True
        stateIndicatingIcon = errorIcon
    elif system_value > float(thresholds.warning):
        hasWarning = True
        stateIndicatingIcon = warningIcon
    updates_info = f"{serverInfo_array['updates']['amount_of_available_updates']} " \
                   f"({serverInfo_array['updates']['updates_available_output']})"
    serverReport += stateIndicatingIcon + f"<b>Available Updates:</b> {preformatted(updates_info)}\n"

    # Add System Restart information with an if-else statement.
    thresholds = get_thresholds('system_restart')
    stateIndicatingIcon = ""
    system_value = float(serverInfo_array['system_restart']['time_elapsed_seconds'])
    if system_value > timeStringUtils.convert_time_string_to_seconds(thresholds.error):
        hasError = True
        stateIndicatingIcon = errorIcon
    elif system_value > timeStringUtils.convert_time_string_to_seconds(thresholds.warning):
        hasWarning = True
        stateIndicatingIcon = warningIcon
    restart_info = "No system restart required" if serverInfo_array['system_restart']['status'] == 'No' else \
        f"System restart required for {preformatted(serverInfo_array['system_restart']['time_elapsed_human_readable'])}"
    serverReport += stateIndicatingIcon + f"<b>System Restart:</b> {preformatted(restart_info)}\n"

    # Add Linux Server State Tool information.
    tool_info = ""
    thresholds = get_thresholds('linux_server_state_tool')
    stateIndicatingIcon = ""
    # Check remote connection.
    if serverInfo_array['linux_server_state_tool']['repo_accessible'] == "True":

        # Check local changes.
        if serverInfo_array['linux_server_state_tool']['local_changes'] == "Yes":
            tool_info += "Uncommitted local changes, "

        # Is repo up to date?
        git_behind_count = int(serverInfo_array['linux_server_state_tool']['behind_count'])
        if git_behind_count > 0:
            
            system_value = float(serverInfo_array['linux_server_state_tool']['behind_count'])
            if system_value > float(thresholds.error):
                hasError = True
                stateIndicatingIcon = errorIcon
            elif system_value > float(thresholds.warning):
                hasWarning = True
                stateIndicatingIcon = warningIcon

            tool_info += f"Repo updateable. {git_behind_count} commits behind."
        else:
            tool_info += f"Tool is up to date"
    else:
        tool_info += "Remote repo Not accessible!! Check connection!! repo_accessible: " + serverInfo_array['linux_server_state_tool']['repo_accessible'] 

    serverReport += f"<b>Linux Server State Tool:</b> {preformatted(tool_info)}\n"

    
    # Determine overall server state, adapt heading and concenate with rest of report.
    stateIndicatingIcon = ""
    if hasError == True:
        stateIndicatingIcon = errorIcon
    elif hasWarning == True:
        stateIndicatingIcon = warningIcon
    serverHeading = stateIndicatingIcon + f"<b>Server Status Report</b> - {preformatted(serverName)}\n"
    serverReport = serverHeading + serverReport

    return ServerReport(serverReport, hasWarning=hasWarning, hasError=hasError)

class Thresholds:
    def __init__(self, warning: str, error: str):
        self.warning = warning
        self.error = error

class ThresholdStatus(Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"

def get_thresholds(thresholds_key: str) -> Thresholds:
    # Helper function to get the thresholds from the config
    warning = config_array['thresholds'][thresholds_key]['warning']
    error = config_array['thresholds'][thresholds_key]['error']
    return Thresholds(warning, error)


# Function to check if the repository is accessible.
def is_repo_accessible(repo_url):
    # You can use your own logic to check repository accessibility.
    # For simplicity, I'm assuming the repository is accessible if the URL is provided.
    return bool(repo_url)

# Function to check if there are local changes.
def has_local_changes():
    # You can use your own logic to check for local changes.
    # For simplicity, I'm assuming there are local changes if 'local_changes' is not 'None'.
    return serverInfo_array['linux_server_state_tool']['local_changes'] != 'None'

