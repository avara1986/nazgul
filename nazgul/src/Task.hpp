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

namespace models {
    class Task {
    private:
        sqlite3 *db{};

        static void getDatetimeNow(char* datetime_string) {
            // Current time
            time_t t = time(nullptr);

            // Time to strign
            tm* curr_tm = localtime(&t);
            strftime(datetime_string, 50, "%Y-%m-%d %T", curr_tm);
        }

    public:
        Task();

        Task(int x0, int y0, int x1, int y1);

        ~Task();

        int connect(char *db_path);

        void close();

        int createDb();

        int insert(char *msg, char *kind);

        int get();

        void create(char *msg, char *kind);

        void move(int dx, int dy);

        static int callback(void *NotUsed, int argc, char **argv, char **azColName) {
            int i;
            for (i = 0; i < argc; i++) {
                printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
            }
            printf("\n");
            return 0;
        }

        static int select_callback(void *data, int argc, char **argv, char **azColName){
            int i;
            fprintf(stderr, "%s: ", (const char*)data);

            for(i = 0; i<argc; i++){
                printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
            }

            printf("\n");
            return 0;
        }
    };
}

#endif