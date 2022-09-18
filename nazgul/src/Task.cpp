#include "Task.hpp"

using namespace std;

int Task::connect(string db_path) {
    int rc;

    rc = sqlite3_open(db_path.c_str(), &db);

    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return -1;
    } else {
        // fprintf(stderr, "Opened database successfully\n");
    }
    return 0;
}

void Task::close() {
    sqlite3_close(db);
}

int Task::createDb() {
    char *zErrMsg = nullptr;
    int rc;
    const char *sql = "CREATE TABLE tasks" \
      "(id integer primary key, ts timestamp, msg text, kind_type varchar, check_type varchar)";

    /* Execute SQL statement */
    rc = sqlite3_exec(db, sql, NULL, 0, &zErrMsg);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(stdout, "Table created successfully\n");
    }
    return 0;
}

int Task::insert(const string& msg, const string& kind, string check) {
    sqlite3_stmt *stmt;
    int rc;
    char *zErrMsg = nullptr;
    const char *istmt = "INSERT INTO tasks(ts, msg, kind_type, check_type) VALUES (?, ?, ?, ?);";

    /* Validate type of check */
    auto check_last_check_type = getOnceByMsg(msg);
    if (!check_last_check_type.empty()) {
        if(check_last_check_type[0].check == CHECKIN){
            check = CHECKOUT;
        }
    }

    /* Get Datetime now */
    char time_now[19];
    _getDatetimeNow(time_now);

    /* Prepare SQL statement */
    rc = sqlite3_prepare_v2(db, istmt, strlen(istmt), &stmt, nullptr);
    assert(rc == SQLITE_OK);
    sqlite3_bind_text(stmt, 1, time_now, strlen(time_now), NULL);
    sqlite3_bind_text(stmt, 2, msg.c_str(), strlen(msg.c_str()), NULL);
    sqlite3_bind_text(stmt, 3, kind.c_str(), strlen(kind.c_str()), NULL);
    sqlite3_bind_text(stmt, 4, check.c_str(), strlen(check.c_str()), NULL);

    /* Execute SQL statement */
    rc = sqlite3_step(stmt);

    /* Check result */
    if (rc != SQLITE_DONE) {
        fprintf(stderr, "SQL INSERT error(%d): %s\n", rc, zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        // fprintf(stdout, "Tasks created successfully\n");
    }
    sqlite3_reset(stmt);
    return 0;
}

inline vector<task> Task::query(const string& sql) {
    char *zErrMsg = nullptr;
    int rc;
    results = {};

    /* Execute SQL statement */
    rc = sqlite3_exec(db, sql.c_str(), _selectCallback, (void *) this, &zErrMsg);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\nQUERY: %s\n", zErrMsg, sql.c_str());
        sqlite3_free(zErrMsg);
    } else {
        // fprintf(stdout, "Select done successfully\n");
    }

    return results;
}

vector<task> Task::getAll() {
    string sql = "SELECT * FROM tasks order by ts desc";
    return query(sql);
}

vector<task> Task::getWorkdays(string from_date, string to_date) {
    string sql = "SELECT * FROM tasks WHERE kind_type = 'workday' ORDER BY ts DESC";
    if (from_date != "" && to_date != ""){
        sql = "SELECT * FROM tasks WHERE kind_type = 'workday' AND ts >= '" + from_date + "' AND ts <= '" + to_date + "' ORDER BY ts DESC";
    }

    return query(sql);
}

vector<task> Task::getTaskOfWorkdays(string date_start, string date_end) {
    string sql = "SELECT * FROM tasks WHERE kind_type != 'workday' AND ts >= '" + date_start + "' AND ts <= '" + date_end + "' ORDER BY ts DESC";
    return query(sql);
}

vector<task> Task::getOnceByMsg(string msg) {
    string sql = "SELECT * FROM tasks WHERE msg='" + msg + "' ORDER BY ts DESC LIMIT 0,1";
    return query(sql);
}


int main(int argc, char *argv[]) {
    auto t = Task();
    t.connect("nazgul.db");
    t.createDb();
    t.insert("workday", "workday", CHECKIN);
    auto results = t.getAll();
    for(auto result: results){
        cout << "ID = " << result.id << std::endl;
        cout << "timestamp = " << result.timestamp << std::endl;
        cout << "msg = " << result.msg << std::endl;
        cout << "check = " << result.check << std::endl;
        cout << "kind = " << result.kind << std::endl;
        printf("-------------\n");
    }
    t.close();
    return 0;
}