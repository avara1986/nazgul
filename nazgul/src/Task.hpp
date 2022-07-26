#ifndef MODELS_H
#define MODELS_H

#include <iostream>
#include <iomanip>
#include <ctime>
#include <sqlite3.h>
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cassert>
#include <vector>

#define CHECKIN "checkin"
#define CHECKOUT "checkout"


using namespace std;

typedef struct _task task;

struct _task
{
    string id;
    string timestamp;
    string msg;
    string kind;
    string check;
};

class Task {
private:
    sqlite3 *db{};
    vector<task> results;

    static void _getDatetimeNow(char* datetime_string) {
        // Current time
        time_t t = time(nullptr);

        // Time to strign
        tm* curr_tm = localtime(&t);
        strftime(datetime_string, 50, "%Y-%m-%d %T", curr_tm);
    }

    static int _selectCallback(void *data, int argc, char **argv, char **azColName){
        Task* task_inst = static_cast<Task*>(data);
        // printf("_selectCallback called");
        task result{argv[0], argv[1] ? argv[1] : "NULL", argv[2], argv[3], argv[4]};
        task_inst->results.push_back(result);
        return 0;
    }

public:
    // Default constructor
    Task() = default;

    // Destructor
    ~Task() = default;

    int connect(string db_path);

    void close();

    int createDb();

    int insert(const string& msg, const string& kind){
        return insert(msg, kind, CHECKIN);
    };

    int insert(const string& msg, const string& kind, string check);

    vector<task> getAll();

    vector<task> getOnceByMsg(string msg);

    vector<task> getWorkdays();

    vector<task> getTaskOfWorkdays(string date_start, string date_end);

    inline vector<task> query(const string& sql);
};


#endif