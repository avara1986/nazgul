from nazgul.driver import Driver
from nazgul.manager import Manager


class DriverMessage(Driver):
    user = ""
    user_id = ""
    text = ""
    msg = {}

    def parse_request(self, request):
        self.msg = request.get_json()

    def set_values(self):
        self.user = self.msg["user"]["displayName"]
        self.user_id = self.msg["user"]["name"]
        self.text = self.msg["message"]["text"]

    def is_valid_msg(self):
        return False

    def trigger(self, request):
        self.parse_request(request)
        return self.is_valid_msg()


class MessageManager(Manager):
    class_to_import = "Message"
    path_to_search = "messages"
    module_to_search = "nazgul.messages.{module}"

    def get(self):
        msg = self.get_by_trigger()
        if msg:
            msg.set_values()
        return msg
