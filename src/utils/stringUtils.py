## Utilities around strings.

# Split string so that every opening tag has its closing tag and every string is shorter than 4096 chars
# If string contains list of products, it tries to keep products together.
def splitLongTextIntoWorkingMessages(messageToSplit):
	individualMessagesToSend = []
	if len(messageToSplit) < 4096:
		individualMessagesToSend.append(messageToSplit)
		return individualMessagesToSend
	else:
		# Try to split message keeping elements grouped by ID together
		if "🔸" in messageToSplit: 

			groupedItems = messageToSplit.split("🔸")
			currentIndividualMessage = ""
			potentialIndividualMessage = ""

			for item in groupedItems:

				# Do not add 🔸 to message if item does not start with "<b>ID:" .
				if (not item.startswith("Tool <b>") and not item.startswith(" <i><b>") ):
					potentialIndividualMessage += item
				else:
					potentialIndividualMessage += "🔸" + item

				if len(potentialIndividualMessage) < 4096:
					currentIndividualMessage = potentialIndividualMessage
				else:
					individualMessagesToSend.append(currentIndividualMessage)
					currentIndividualMessage = ""
					potentialIndividualMessage = "🔸" + item

			# Add last item.
			individualMessagesToSend.append(potentialIndividualMessage)
					
		else:
			# Split Message by new line breaks.
			groupedItems = messageToSplit.split("\n")
			currentIndividualMessage = ""
			potentialIndividualMessage = ""

			for item in groupedItems:

				potentialIndividualMessage += "\n" + item
					
				if len(potentialIndividualMessage) < 4096:
					currentIndividualMessage = potentialIndividualMessage
				else:
					individualMessagesToSend.append(currentIndividualMessage)
					currentIndividualMessage = ""
					potentialIndividualMessage = "\n" + item

			# Add last item.
			individualMessagesToSend.append(potentialIndividualMessage)

		# Return messages.
		return individualMessagesToSend

		