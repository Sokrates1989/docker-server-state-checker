## Utilities for telegram usage such as sending messages.

# For getting current timestamp.
import time
# For file operations with operating system.
import os
# For getting config.
import json
# For creating files.
import fileUtils
# To interact with telgram bots.
import telebot

## Own classes.
import stringUtils

# Config file.
config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config/", "config.txt")
config_file = open(config_file_pathAndName)
config_array = json.load(config_file)

# Fetch botToken from secret file, if existing.
try:
    BOT_TOKEN_FILE = os.getenv("botToken_FILE")
    with open(f"{BOT_TOKEN_FILE}", "r") as bot_token_file:
        botToken = bot_token_file.read().strip()
finally:
    # If there is no botToken_FILE.
    if not botToken:
        botToken = os.getenv('botToken').strip().strip("\"") or config_array["telegram"]["botToken"].strip().strip("\"")

# Initialize telegram bot.
bot = telebot.TeleBot(botToken, parse_mode="HTML")

# Telegram Chats were to send info, error and warnings to.
errorChatIDs_configString = os.getenv('errorChatIDs') or config_array["telegram"]["errorChatIDs"]
warningChatIDs_configString = os.getenv('warningChatIDs') or config_array["telegram"]["warningChatIDs"]
infoChatIDs_configString = os.getenv('infoChatIDs') or config_array["telegram"]["infoChatIDs"]

# Get individual chat IDs (raw/ unoptimized).
errorChatIDs = errorChatIDs_configString.split(',')
warningChatIDs = warningChatIDs_configString.split(',')
infoChatIDs = infoChatIDs_configString.split(',')

# Sanitize chat IDs (remove " and spaces from value).
errorChatIDs = [chat_id.strip().strip('"') for chat_id in errorChatIDs]
warningChatIDs = [chat_id.strip().strip('"') for chat_id in warningChatIDs]
infoChatIDs = [chat_id.strip().strip('"') for chat_id in infoChatIDs]

# Ensure, that there is at least one item in each chat-group.
if not any(errorChatIDs):
    raise ValueError("At least one item is required in errorChatIDs.")
if not any(warningChatIDs):
    raise ValueError("At least one item is required in warningChatIDs.")
if not any(infoChatIDs):
    raise ValueError("At least one item is required in infoChatIDs.")



# Send Error message.
def sendErrorMessage(errorMessage):
    for errorChatID in errorChatIDs:
        sendMessage(errorChatID, errorMessage)

# Send Warning message.
def sendWarningMessage(warningMessage):
    for warningChatID in warningChatIDs:
        sendMessage(warningChatID, warningMessage)

# Send Info message.
def sendInfoMessage(infoMessage):
    for infoChatID in infoChatIDs:
        sendMessage(infoChatID, infoMessage)

# Send message using telegram.
def sendMessage(chatID, message):

    # Recreate bot to avoid timeout errors.
    bot = telebot.TeleBot(botToken, parse_mode="HTML")
    
    # Does message have to be split?
    if len(message) > 4096:
        # Split message.
        individualMessages = stringUtils.splitLongTextIntoWorkingMessages(message)

        # Send messages.
        for individualMessage in individualMessages:
            bot.send_message(chatID, individualMessage)

    else:
        bot.send_message(chatID, message)
