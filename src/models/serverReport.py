## Model used to wrap serverState Info.

# To create enumerations.
from enum import Enum

# Own classes.
class MostCrucialServerState(Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


class ServerReport:

	# Constructor.
	def __init__(self, serverReportMessage, hasWarning=False, hasError=False):

		self._serverReportMessage = serverReportMessage
		self._hasWarning = hasWarning
		self._hasError = hasError

	def getServerReportMessage(self):
		return self._serverReportMessage
	
	def getMostCrucialState(self) -> MostCrucialServerState:
		if self.hasError():
			return MostCrucialServerState.ERROR
		else:
			if self.hasWarning():
				return MostCrucialServerState.WARNING
			else:
				return MostCrucialServerState.INFO

	def hasWarning(self) -> bool:
		return self._hasWarning

	def hasError(self) -> bool:
		return self._hasError
