#include "Task.hpp"

using namespace std;

#define CHECKIN "checkin"
#define CHECKOUT "checkout"

namespace models {

    // Default constructor
    Task::Task() {}

    // Destructor
    Task::~Task() = default;

    int Task::connect(char *db_path) {
        int rc;

        rc = sqlite3_open(db_path, &db);

        if (rc) {
            fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
            return -1;
        } else {
            fprintf(stderr, "Opened database successfully\n");
        }
        return 0;
    }

    void Task::close() {
        sqlite3_close(db);
    }

    int Task::createDb() {
        char *zErrMsg = 0;
        int rc;
        const char *sql = "CREATE TABLE tasks" \
          "(id integer primary key, ts timestamp, msg text, kind varchar)";

        /* Execute SQL statement */
        rc = sqlite3_exec(db, sql, callback, 0, &zErrMsg);

        if (rc != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", zErrMsg);
            sqlite3_free(zErrMsg);
        } else {
            fprintf(stdout, "Table created successfully\n");
        }
        return 0;
    }

    int Task::insert(char *msg, char *kind = CHECKIN) {
        char *zErrMsg = nullptr;
        int rc;
        const char *istmt = "INSERT INTO tasks(ts, msg, kind) VALUES (?, ?, ?);";
        sqlite3_stmt *stmt;

        const char *ozTest;
        rc = sqlite3_prepare_v2(db, istmt, strlen(istmt), &stmt, &ozTest);
        assert(rc == SQLITE_OK);
        /* Prepare SQL statement */
        char time_now[19];
        getDatetimeNow(time_now);
        sqlite3_bind_text(stmt, 1, time_now, strlen(time_now), NULL);
        sqlite3_bind_text(stmt, 2, msg, strlen(msg), NULL);
        sqlite3_bind_text(stmt, 3, kind, strlen(kind), NULL);

        /* Execute SQL statement */
        rc = sqlite3_step(stmt);

        if (rc != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", zErrMsg);
            sqlite3_free(zErrMsg);
        } else {
            fprintf(stdout, "Tasks created successfully\n");
        }
        sqlite3_reset(stmt);
        return 0;
    }

    int Task::get() {
        char *zErrMsg = 0;
        int rc;
        const char *sql = "SELECT * FROM tasks";
        const char *data = "Callback function called";

        /* Execute SQL statement */
        rc = sqlite3_exec(db, sql, select_callback, (void *) data, &zErrMsg);

        if (rc != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", zErrMsg);
            sqlite3_free(zErrMsg);
        } else {
            fprintf(stdout, "Select done successfully\n");
        }
        sqlite3_close(db);
        return 0;


    }
}


int main(int argc, char *argv[]) {
    auto t = models::Task();
    t.connect("nazgul.db");
    // t.createDb();
    t.insert("workday", "checkin");
    t.get();
    t.close();
    return 0;
}