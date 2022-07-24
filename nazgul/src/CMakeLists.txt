cmake_minimum_required(VERSION 3.22)
project(tasks)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_BUILD_TYPE Debug)

add_compile_options(-fPIC -fexceptions -fvisibility=hidden -pthread -Wall -Wwrite-strings)

# Dependencies
find_package (SQLite3)

# Create Executable
include_directories(.)

add_executable(tasks
        Task.cpp
        Task.hpp)

# Link dependencies
include_directories(${SQLite3_INCLUDE_DIRS})
target_link_libraries(tasks ${SQLite3_LIBRARIES})