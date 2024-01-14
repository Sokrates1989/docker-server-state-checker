# Model used to wrap information about the states of the tools to check.

class ToolStateItem:

	# Constructor.
	def __init__(self, name, toolIsUp, toolIsDownMessageHasBeenSent, description = ""):

		# Convert toolIsDownMessageHasBeenSent to boolean.
		if toolIsDownMessageHasBeenSent == 0 or toolIsDownMessageHasBeenSent == False:
			toolIsDownMessageHasBeenSent = False
		if toolIsDownMessageHasBeenSent == 1 or toolIsDownMessageHasBeenSent == True:
			toolIsDownMessageHasBeenSent = True

		# Convert toolIsUp to boolean.
		if toolIsUp == 0:
			toolIsUp = False
		if toolIsUp == 1:
			toolIsUp = True

		# Ensure descriptions is not None.
		if description == None or description == "None" :
			description = ""

		self.name = name
		self.description = description
		self.toolIsUp = toolIsUp
		self.toolIsDownMessageHasBeenSent = toolIsDownMessageHasBeenSent
		self.statusMessage = ""
		self.isCustomCheck = False
		self.isBackupCheck = False
		self.checkingEveryXMinutes = None


	# Add statusMessage.
	def setStatusMessage(self, statusMessage):
		self.statusMessage = statusMessage


	# Indicate, that checked tool is a custom check.
	def indicateThatToolIsCustom(self):
		self.isCustomCheck = True


	# Indicate, that checked tool is a backup check.
	def indicateThatToolIsBackup(self):
		self.isBackupCheck = True


	# Set frequency of tool check.
	def setCheckFrequency(self, checkingEveryXMinutes):
		self.checkingEveryXMinutes = checkingEveryXMinutes


	def asMap(self):
		return {
			"name": self.name,
			"description": self.description,
			"toolIsUp": self.toolIsUp,
			"toolIsDownMessageHasBeenSent": self.toolIsDownMessageHasBeenSent,
			"statusMessage": self.statusMessage,
			"isCustomCheck": self.isCustomCheck,
			"isBackupCheck": self.isBackupCheck,
			"checkingEveryXMinutes": self.checkingEveryXMinutes,
		}
