#!/bin/bash

mkdir build libs
cd build

# Генерируем файлы сборки с помощью CMake
cmake ..

# Собираем библиотеку
make

make install

# Возвращаемся в исходную директорию
cd ..