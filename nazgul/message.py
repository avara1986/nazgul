import json
import os

from nazgul.driver import Driver
from nazgul.manager import Manager


class DriverMessage(Driver):
    user_name = ""
    user_id = ""
    text = ""
    msg = {}
    users = json.loads(os.environ.get("USERS", '{}'))
    use_ids = False

    @property
    def user(self):
        if self.use_ids:
            return "<{}>".format(self.user_id)
        return self.user_name


    def parse_request(self, request):
        self.msg = request.get_json()

    def set_values(self):
        pass

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
