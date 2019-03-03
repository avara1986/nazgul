from nazgul.message import DriverMessage
from nazgul.response import GoogleChatResponse


class Message(DriverMessage):
    response = GoogleChatResponse

    def set_values(self):
        self.user = self.msg["user"]["displayName"]
        self.user_id = self.msg["user"]["name"]
        self.text = self.msg["message"]["text"]

    def is_valid_msg(self):
        return self.msg.get("message", False) and self.msg.get("message", {}).get("text", False)
