from nazgul.message import DriverMessage
from nazgul.response import GoogleActionResponse


class Message(DriverMessage):
    response = GoogleActionResponse
    use_ids = False

    def set_values(self):
        self.user_id = self.msg["originalDetectIntentRequest"]["payload"]["user"]["userId"]
        self.user_name = self.users.get(self.user_id, {}).get("name", "")
        if self.users[self.user_id]["alias"]:
            self.user_id = self.users[self.user_id]["alias"]

        self.text = self.msg["queryResult"]["queryText"]

    def is_valid_msg(self):
        return self.msg.get("queryResult", False) and self.msg.get("queryResult", {}).get("queryText", False)
