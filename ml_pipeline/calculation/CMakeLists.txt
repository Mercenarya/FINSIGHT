cmake_minimum_required(VERSION 3.20)

# Project
project(Evaluate CXX)

# Standardize
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Adding sources
set(
    SOURCES
    calculation/ profitability.cpp
)

# Requires package
find_package(pybind11 REQUIRED)

# Last module processing
pybind11_add_module(
    evaluate_module
    ${SOURCES}
)
