import datetime
from random import randint

from nazgul.action import DriverAction
from nazgul.constants import CHECKIN, CHECKOUT
from nazgul.models.datastore import list_objects, create

CHECKIN_MESSAGES = ["Welcome!", "Que comience el juego!", "Valar morghulis!"]
CHECKOUT_MESSAGES = ["Que la fuerza te acompañe!", "Foco y coraje!"]


class Action(DriverAction):
    action_name = "Saluda, sin más"

    message = None

    triggers = ["hola", "hola!", "adios", "adios!"]

    @property
    def help(self):
        return "Te saluda y te despide"

    def response(self):
        message_1 = ""
        message_2 = ""
        if "adios" in self.message.text.lower():
            message_1 = "Hasta luego"
            message_2 = CHECKOUT_MESSAGES[randint(0, len(CHECKOUT_MESSAGES) - 1)]
        elif "hola" in self.message.text.lower():
            message_1 = "Buenas"
            message_2 = CHECKIN_MESSAGES[randint(0, len(CHECKOUT_MESSAGES) - 1)]

        return "{} <{}>. {}. teclea 'r' o 'registrar' para registrar entrada y salida automáticamente.".format(message_1, self.message.user_id, message_2)
