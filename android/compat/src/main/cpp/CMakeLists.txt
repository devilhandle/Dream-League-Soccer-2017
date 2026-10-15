cmake_minimum_required(VERSION 3.22.1)
project(dls17_compat LANGUAGES C CXX)

add_library(dls17_compat SHARED compat_probe.cpp)

target_compile_features(dls17_compat PRIVATE cxx_std_17)
target_compile_options(dls17_compat PRIVATE -Wall -Wextra -Werror)
find_library(log-lib log)
target_link_libraries(dls17_compat PRIVATE ${log-lib})
