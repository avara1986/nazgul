import datetime

from _task cimport Task, vector, task, string

cdef string CHECKIN = "checkin"
cdef string CHECKOUT = "checkout"

cdef class Nazgul():
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

    cpdef void insert_task(self, msg: str, kind):
        cdef Task t = Task()
        t.connect(self.db_path.encode('utf-8'))
        t.insert(msg.encode('utf-8'), kind.encode('utf-8'))

    cpdef void print_tasks(self):
        cdef Task t = self.init_db()
        results = t.getAll()
        for result in results:
            print(b"ID = " + result.id)
            print(b"timestamp = " + result.timestamp)
            print(b"msg = " + result.msg)
            print(b"check = " + result.check)

    cpdef vector[task] get_tasks(self):
        cdef Task t = self.init_db()
        return t.getAll()

    cpdef str get_week_tasks(self):
        now = datetime.datetime.now()
        week_start = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = (week_start + datetime.timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)

        message = "*Recuperando datos de la semana del {} al {}*\n".format(week_start.strftime("%Y-%m-%d"),
                                                                           week_end.strftime("%Y-%m-%d"))
        total_hours = 0

        cdef Task t = self.init_db()
        cdef vector[task] results = t.getAll()

        for i in range(0, results.size()):
            try:
                if results[i].check == CHECKOUT and results[i + 1].check == CHECKIN:
                    s_from = results[i + 1].timestamp
                    date_from = datetime.datetime.strptime(s_from.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                    s_to = results[i].timestamp
                    date_to = datetime.datetime.strptime(s_to.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
                    hours = (date_to - date_from).seconds / 3600
                    total_hours += hours
                    message += "*[{date_from} - {date_to}]:* {hours}\n".format(date_from=s_from, date_to=s_to,
                                                                               hours=hours)
            except IndexError as e:
                print("ERROR: %s" % e)
        return message

cdef void main():
    cdef Task t = Task()
    t.connect("example.db")
    t.createDb()
    t.insert("workday", CHECKIN)
    results = t.getAll()
    for result in  results:
        print("ID = " + result.id)
        print("timestamp = " + result.timestamp)
        print("msg = " + result.msg)
        print("check = " + result.check)
    t.close()

