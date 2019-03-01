import datetime

from nazgul.action import DriverAction
from nazgul.constants import CHECKIN, CHECKOUT
from nazgul.models.datastore import list_objects

CHECKIN_MESSAGES = ["Welcome!", "Que comience el juego!", "Valar morghulis!"]
CHECKOUT_MESSAGES = ["Que la fuerza te acompañe!", "Foco y coraje!"]


class Action(DriverAction):
    action_name = "Tiempo invertido esta semana"

    message = None

    triggers = ['horas', ]

    @property
    def help(self):
        return "Teclea 'horas' para ver cuanto tiempo has invertido cada día"

    def get_hours_user(self, user_id):
        now = datetime.datetime.now()
        week_start = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = (week_start + datetime.timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)

        results = list_objects(user=user_id, filters=(
            ("timestamp", ">", week_start),
            ("timestamp", "<", week_end),
        ), limit=50)
        message = "*Recuperando datos de la semana del {} al {}*\n".format(week_start.strftime("%Y-%m-%d"),
                                                                           week_end.strftime("%Y-%m-%d"))
        total_hours = 0
        for i in range(0, len(results)):
            try:
                if results[i]["type"] == CHECKOUT and results[i + 1]["type"] == CHECKIN:
                    date_from = results[i + 1]["timestamp"]
                    date_to = results[i]["timestamp"]
                    hours = (date_to - date_from).seconds / 3600
                    total_hours += hours
                    message += "*[{date_from} - {date_to}]:* {hours}\n".format(date_from=date_from, date_to=date_to,
                                                                               hours=hours)
            except IndexError:
                pass
        return message, total_hours

    def response(self):
        message, total_hours = self.get_hours_user(self.message.user_id)
        message += "*TOTAL: {}*".format(total_hours)
        return message
