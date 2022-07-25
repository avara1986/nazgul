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

using namespace std;

typedef struct _task task;

struct _task
{
    string id;
    string timestamp;
    string msg;
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
        task result{argv[0], argv[1] ? argv[1] : "NULL", argv[2], argv[3]};
        task_inst->results.push_back(result);
        return 0;
    }

    inline vector<task> _select(const string& sql);

public:
    // Default constructor
    Task() = default;

    // Destructor
    ~Task() = default;

    int connect(string db_path);

    void close();

    int createDb();

    int insert(string msg, string check);

    vector<task> getAll();

    vector<task> getOnceByMsg(string msg);
};


#endif