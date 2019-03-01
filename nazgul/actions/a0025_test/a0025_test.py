from nazgul.actions.a0020_get_time_per_day.a0020_get_time_per_day import Action as HoursWeekAction

CHECKIN_MESSAGES = ["Welcome!", "Que comience el juego!", "Valar morghulis!"]
CHECKOUT_MESSAGES = ["Que la fuerza te acompañe!", "Foco y coraje!"]


class Action(HoursWeekAction):
    action_name = "Test"

    message = None

    triggers = ['test', ]

    @property
    def help(self):
        return "Test"

    def response(self):
        return "test"
