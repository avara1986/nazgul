from nazgul.message import DriverMessage
from nazgul.response import GoogleActionResponse


class Message(DriverMessage):
    response = GoogleActionResponse

    def set_values(self):
        self.user = ""
        self.user_id = self.msg["originalDetectIntentRequest"]["payload"]["user"]["userId"]
        self.text = self.msg["queryResult"]["queryText"]

    def is_valid_msg(self):
        return self.msg.get("queryResult", False) and self.msg.get("queryResult", {}).get("queryText", False)
