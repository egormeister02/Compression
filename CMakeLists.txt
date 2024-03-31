cmake_minimum_required(VERSION 3.10)
project(load_dump)

set(SOURCES source/load_dump.cpp)

add_library(load_dump STATIC ${SOURCES})

set(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR})

install(TARGETS load_dump DESTINATION ../libs/)