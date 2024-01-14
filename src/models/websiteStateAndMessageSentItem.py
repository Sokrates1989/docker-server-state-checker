# Model to wrap state of website and whether that state has been sent to admin.

# To convert class to json and back.
import json


class WebsiteStateAndMessageSentItem:

    # Constructor.
    def __init__(self, websiteState="Down", messageHasBeenSent=True):
        self.websiteState = websiteState
        self.messageHasBeenSent = messageHasBeenSent

    def asMap(self):
        return {
            "websiteState": self.websiteState,
            "messageHasBeenSent": self.messageHasBeenSent,
        }

    def toJson(self):
        return json.dumps(self.asMap())


    # Checks, if the newly received website state has already been sent based on classes values.
    def isMessageIsDownMessageLastSentMessage(self):
        if self.websiteState == "Down" and self.messageHasBeenSent == True:
            return True
        else:
            return False


    @staticmethod
    def fromJson(jsonString):
        asMap = json.loads(jsonString)
        return WebsiteStateAndMessageSentItem(websiteState=asMap["websiteState"],
                                              messageHasBeenSent=asMap["messageHasBeenSent"])
