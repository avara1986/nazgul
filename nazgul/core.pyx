import datetime

from _task cimport Task, string, task, vector, week_report, day_report, task_report


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


    cdef int update_day(self, Task t, day_report& day_result, string s_from, string s_to) except? -1:
        date_from = datetime.datetime.strptime(s_from.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
        date_to = datetime.datetime.strptime(s_to.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
        hours_workday = (date_to - date_from).seconds / 3600
        day_result.start = s_from
        day_result.end = s_to
        day_result.total_time = hours_workday
        day_result.rest_time = 0.0
        
        cdef vector[task] tasks_and_breaks = t.getTaskOfWorkdays(day_result.start, day_result.end)
        cdef task_report task_result

        for j in range(0, tasks_and_breaks.size()):
            if tasks_and_breaks[j].check == CHECK_OUT and tasks_and_breaks[j + 1].check == CHECK_IN:
                task_result = {}
                s_from = tasks_and_breaks[j + 1].timestamp
                date_from = datetime.datetime.strptime(s_from.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                s_to = tasks_and_breaks[j].timestamp
                date_to = datetime.datetime.strptime(s_to.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                hours_break = (date_to - date_from).seconds / 3600
                task_result.start = s_from
                task_result.end = s_to
                task_result._task = tasks_and_breaks[j]
                task_result.total_time = hours_break
                day_result.tasks.push_back(task_result)
                if tasks_and_breaks[j].kind == KIND_BREAK:
                    day_result.rest_time += hours_break
        return 0

    cpdef week_report get_week_tasks(self):
        now = datetime.datetime.now()
        week_start = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = (week_start + datetime.timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)

        message: str = "*Week since {} till {}*\n".format(week_start.strftime("%Y-%m-%d"),
                                                          week_end.strftime("%Y-%m-%d"))
        msg: str = ""
        total_hours = 0

        cdef Task t = self.init_db()
        cdef vector[task] workdays = t.getWorkdays()
        cdef week_report week_result
        cdef day_report day_result
        cdef bint skip_next = False

        for i in range(0, workdays.size()):
            try:
                day_result = {}
                if workdays[i].check == CHECK_OUT and workdays[i + 1].check == CHECK_IN:
                    self.update_day(t, day_result, workdays[i + 1].timestamp, workdays[i].timestamp)
                    total_hours += day_result.total_time
                    skip_next = True
                elif skip_next:
                    skip_next = False
                    continue
                elif workdays[i].check == CHECK_IN:
                    self.update_day(t, day_result, workdays[i].timestamp, <string>bytes(now.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8"))
                    total_hours += day_result.total_time
          
                week_result.days.push_back(day_result)
            except IndexError as e:
                print("ERROR: %s" % e)
        return week_result

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
