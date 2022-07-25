from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "src/Task.hpp":
    ctypedef struct task:
        string id;
        string timestamp;
        string msg;
        string check;

    cdef cppclass Task:
        Task() except +
        int connect(string db_path);
        void close();
        int createDb();
        int insert(string msg);
        int insert(string msg, string check);
        vector[task] getAll();
