import logging
import os
from typing import Text

from nazgul.constants import BOT_NAME
from nazgul.constants import LOGGER_NAME
from nazgul.message import GoogleChatMessage
from nazgul.utils import import_from

logger = logging.getLogger(LOGGER_NAME)


class DriverAction:
    action_name = ""
    triggers = []
    message = GoogleChatMessage

    def __init__(self, *args, **kwargs):
        pass

    @property
    def help(self) -> Text:
        return ""

    def check_triggers_list(self):
        message = self.message.text.lower()
        for trigger in self.triggers:
            if (trigger == message or
                message == ("@{bot_name} {trigger}".format(bot_name=BOT_NAME, trigger=trigger)) or
                message == ("{trigger} @{bot_name}".format(bot_name=BOT_NAME, trigger=trigger))
            ):
                # message.startswith("@{bot_name} {trigger}".format(bot_name=BOT_NAME, trigger=trigger)) or
                # message.startswith("{trigger} @{bot_name}".format(bot_name=BOT_NAME, trigger=trigger))
                return True
        return False

    def trigger(self, message: GoogleChatMessage) -> bool:
        self.message = message
        return self.check_triggers_list()

    def response(self) -> Text:
        return ""


class ActionManager:

    def __init__(self, message, path=__file__):
        self.message = message
        self.path = os.path.dirname(path)

    def get_actions(self):
        return (self.import_action(k) for k in sorted(os.listdir(os.path.join(self.path, "nazgul/actions"))) if
                k not in ['__pycache__', '__init__.py', ])

    def import_action(self, action_file) -> DriverAction:
        action_module = action_file.replace(".py", "")
        action_object = import_from("nazgul.actions.{action}.{action}".format(action=action_module), "Action")
        logger.info("Init action {}".format(action_object))
        return action_object()

    def get_action_response(self):
        for action in self.get_actions():
            if action.trigger(self.message):
                return action.response()

    def get_actions_help(self):
        help_msg = ""
        for action in self.get_actions():
            help_msg += "*[{}]* {}\n".format(action.action_name, action.help)

        return help_msg

    def response(self):
        help_triggers = ['@{bot_name} help'.format(bot_name=BOT_NAME), 'help']
        if self.message.text.lower() in help_triggers:
            return self.get_actions_help()

        return self.get_action_response()
