import datetime

from nazgul.action import DriverAction
from nazgul.constants import CHECKIN, CHECKOUT
from nazgul.models.datastore import list_objects, create


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
            message_2 = "Salida registrada"
        else:
            message_1 = "Buenas"
            type_record = CHECKIN
            message_2 = "Entrada registrada"

        create({"user": self.message.user_id, "username": self.message.user, "type": type_record,
                "timestamp": datetime.datetime.now()})
        return '{}. {}'.format(message_1, message_2)
