from nazgul.action import DriverAction


class Action(DriverAction):
    action_name = "Repetir"

    message = None

    @property
    def help(self):
        return "Si ninguna acción se detectó, repite el mensaje que llegó"

    def trigger(self, message):
        self.message = message
        return True

    def response(self):
        return '{} dijo {}'.format(self.message.user, self.message.text)
