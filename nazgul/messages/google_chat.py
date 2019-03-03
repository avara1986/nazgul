from nazgul.message import DriverMessage
from nazgul.response import GoogleChatResponse


class Message(DriverMessage):
    response = GoogleChatResponse
    use_ids = True

    def set_values(self):
        self.user_id = self.msg["user"]["name"]
        self.user_name = self.users.get(self.user_id, {}).get("name", False)
        if not self.user_name:
            self.user_name = self.msg["user"]["displayName"]
        if self.users.get(self.user_id, {}).get("alias", False):
            self.user_id = self.users[self.user_id]["alias"]

        self.text = self.msg["message"]["text"]

    def is_valid_msg(self):
        return self.msg.get("message", False) and self.msg.get("message", {}).get("text", False)
