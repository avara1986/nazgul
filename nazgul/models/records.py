import sqlite3
import datetime

from nazgul.constants import DB_PATH, CHECKIN


class Tasks():
    def __init__(self, db_path: str = DB_PATH):
        print(f"Connect to DB {DB_PATH}")
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()

    def create_db(self):
        print("Create Table tasks")
        # Create table
        self.cur.execute("""CREATE TABLE tasks
               (id integer primary key, ts timestamp, msg text, kind varchar)""")
        self.con.commit()

    def insert_task(self, msg: str, kind: str = CHECKIN):
        now = datetime.datetime.now()
        with self.con as con:
            con.execute("insert into tasks(ts, msg, kind) values (?, ?, ?)", (now, msg, kind))

    def get_task(self, msg: str, kind: str = CHECKIN):
        with self.con as con:
            rows = con.execute("select * from tasks msg='?' order by ts desc limit 0,1", (msg,)).fetchall()

    def __call__(self):
        print("Nazgul")
