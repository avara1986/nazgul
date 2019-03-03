import logging
from typing import Text

from nazgul.constants import BOT_NAME
from nazgul.constants import LOGGER_NAME
from nazgul.driver import Driver
from nazgul.manager import Manager
from nazgul.message import DriverMessage

logger = logging.getLogger(LOGGER_NAME)


class DriverAction(Driver):
    action_name = ""
    triggers = []
    message = DriverMessage

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

    def trigger(self, message: DriverMessage) -> bool:
        self.message = message
        return self.check_triggers_list()

    def response(self) -> Text:
        return ""


class ActionManager(Manager):
    class_to_import = "Action"
    path_to_search = "actions"
    module_to_search = "nazgul.actions.{module}.{module}"

    def get_actions_help(self):
        help_msg = ""
        for action in self.get_resources():
            help_msg += "*[{}]* {}\n".format(action.action_name, action.help)

        return help_msg

    def response(self):
        help_triggers = ['@{bot_name} help'.format(bot_name=BOT_NAME), 'help']
        if self.trigger_object.text.lower() in help_triggers:
            return self.get_actions_help()

        return self.get_by_trigger().response()
