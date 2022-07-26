import datetime

from _task cimport Task, string, task, vector


cpdef string CHECK_IN = "checkin"
cpdef string CHECK_OUT = "checkout"

cpdef string KIND_WORKDAY = "workday"
cpdef string KIND_BREAK = "break"
cpdef string KIND_LUNCH = "lunch"
cpdef string KIND_TASK = "task"
cpdef string KIND_MEET = "meet"

cdef class Nazgul:
    db_path: str

    def __init__(self, db_path: str):
        self.db_path = db_path

    cdef Task init_db(self):
        cdef Task t = Task()
        t.connect(self.db_path.encode('utf-8'))
        return t

    cpdef void create_db(self):
        cdef Task t = self.init_db()
        print("Create Table tasks")
        # Create table
        t.createDb()

    cpdef void insert_task(self, msg: str, kind: str, check: str):
        cdef Task t = Task()
        t.connect(self.db_path.encode('utf-8'))
        t.insert(msg.encode('utf-8'), kind.encode('utf-8'), check.encode('utf-8'))

    cpdef void print_tasks(self):
        cdef Task t = self.init_db()
        workdays = t.getAll()
        for result in workdays:
            print(b"ID = " + result.id)
            print(b"timestamp = " + result.timestamp)
            print(b"msg = " + result.msg)
            print(b"kind = " + result.kind)
            print(b"check = " + result.check)

    cpdef vector[task] get_tasks(self):
        cdef Task t = self.init_db()
        return t.getAll()

    cpdef dict get_week_tasks(self):
        now = datetime.datetime.now()
        week_start = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = (week_start + datetime.timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)

        message: str = "*Week since {} till {}*\n".format(week_start.strftime("%Y-%m-%d"),
                                                          week_end.strftime("%Y-%m-%d"))
        msg: str = ""
        total_hours = 0

        cdef Task t = self.init_db()
        cdef vector[task] tasks_and_breaks
        cdef vector[task] workdays = t.getWorkdays()
        days_result = {
            "total": 0,
            "days": []
        }

        for i in range(0, workdays.size()):
            try:
                if workdays[i].check == CHECK_OUT and workdays[i + 1].check == CHECK_IN:
                    day_data = {
                        "start": "",
                        "end": "",
                        "total_time": 0,
                        "rest_time": 0,
                        "tasks": []
                    }
                    s_from = workdays[i + 1].timestamp
                    date_from = datetime.datetime.strptime(s_from.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                    s_to = workdays[i].timestamp
                    date_to = datetime.datetime.strptime(s_to.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                    hours_workday = (date_to - date_from).seconds / 3600
                    total_hours += hours_workday
                    day_data["start"] = s_from
                    day_data["end"] = s_to
                    day_data["total_time"] = hours_workday
                    # msg = "* [{date_from} - {date_to}] {msg}:* {hours}\n".format(msg=workdays[i].msg, date_from=s_from, date_to=s_to,
                    #                                                            hours=hours_workday)
                    # print("DEBUG: %s" % msg)
                    # message += msg
                    tasks_and_breaks = t.getTaskOfWorkdays(s_from, s_to)
                    # print("DEBUG: getTaskOfWorkdays  %s" % tasks_and_breaks.size())
                    day_data["tasks"] = []
                    for j in range(0, tasks_and_breaks.size()):
                        if tasks_and_breaks[j].check == CHECK_OUT and tasks_and_breaks[j + 1].check == CHECK_IN:
                            task_data = {
                                "start": "",
                                "end": "",
                                "task": "",
                                "total_time": 0,
                            }
                            s_from = tasks_and_breaks[j + 1].timestamp
                            date_from = datetime.datetime.strptime(s_from.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                            s_to = tasks_and_breaks[j].timestamp
                            date_to = datetime.datetime.strptime(s_to.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                            hours_break = (date_to - date_from).seconds / 3600

                            task_data["start"] = s_from
                            task_data["end"] = s_to
                            task_data["task"] = tasks_and_breaks[j]
                            task_data["total_time"] = hours_break
                            day_data["tasks"].append(task_data)
                            if tasks_and_breaks[j].kind == KIND_BREAK:
                                day_data["rest_time"] += hours_break
                    days_result["days"].append(day_data)
            except IndexError as e:
                print("ERROR: %s" % e)
        return days_result

cdef void main():
    cdef Task t = Task()
    t.connect("example.db")
    t.createDb()
    t.insert("workday", CHECK_IN)
    workdays = t.getAll()
    for result in workdays:
        print("ID = " + result.id)
        print("timestamp = " + result.timestamp)
        print("msg = " + result.msg)
        print("check = " + result.check)
    t.close()
