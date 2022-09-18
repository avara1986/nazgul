from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "src/Task.hpp":
    ctypedef struct task:
        string id
        string timestamp
        string msg
        string kind
        string check

    cdef cppclass Task:
        Task() except +
        int connect(string db_path);
        void close();
        int createDb();
        int insert(string msg);
        int insert(string msg, string kind);
        int insert(string msg, string kind, string check);
        vector[task] getAll();
        vector[task] getWorkdays(string from_date, string to_date);
        vector[task] getTaskOfWorkdays(string date_start, string date_end)

ctypedef struct task_report:
    string start
    string end
    float total_time
    task _task

ctypedef struct day_report:
    string start
    string end
    float total_time
    float rest_time
    vector[task_report] tasks

ctypedef struct week_report:
    float total
    vector[day_report] days
