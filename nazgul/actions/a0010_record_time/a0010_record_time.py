import datetime
from random import randint

from nazgul.action import DriverAction
from nazgul.constants import CHECKIN, CHECKOUT
from nazgul.models.datastore import list_objects, create

CHECKIN_MESSAGES = ["Welcome!", "Que comience el juego!", "Valar morghulis!"]
CHECKOUT_MESSAGES = ["Que la fuerza te acompañe!", "Foco y coraje!"]


class Action(DriverAction):
    action_name = "Registrar entradas y salidas"

    message = None

    triggers = ['r', 'registrar', "hola", "hola!", "adios", "adios!"]

    @property
    def help(self):
        return "teclea 'r', 'R' o 'registrar' para registrar entrada y salida automáticamente"

    def response(self):
        results = list_objects(user=self.message.user_id)
        if len(results) > 0 and results[0]["type"] == CHECKIN:
            type_record = CHECKOUT
            message_1 = "Hasta luego"
            message_2 = CHECKOUT_MESSAGES[randint(0, len(CHECKOUT_MESSAGES) - 1)]
        else:
            message_1 = "Buenas"
            type_record = CHECKIN
            message_2 = CHECKIN_MESSAGES[randint(0, len(CHECKOUT_MESSAGES) - 1)]

        create({"user": self.message.user_id, "username": self.message.user, "type": type_record,
                "timestamp": datetime.datetime.now()})
        return '{} <{}>. {}'.format(message_1, self.message.user_id, message_2)
