cmake_minimum_required(VERSION 3.20)

# Project
project(Evaluate CXX)

# Standardize
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Adding sources
set(
    SOURCES
    calculation/ _evaluate.cpp
    calculation/ profitability.cpp
    calculation/ liquidity.cpp
    calculation/ efficiency.cpp
)

# Requires package
find_package(pybind11 REQUIRED)

# Last module processing
pybind11_add_module(evaluate_module ${SOURCES})

# set_target_properties(evaluate_module PROPERTIES
#     LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/calculation/build"
# )
# cmake_minimum_required(VERSION 3.14)
# project(evaluate_module LANGUAGES CXX)

# set(CMAKE_CXX_STANDARD 17)
# set(CMAKE_CXX_STANDARD_REQUIRED ON)

# # Fix warning pybind11
# set(PYBIND11_FINDPYTHON ON)

# find_package(Python3 COMPONENTS Development REQUIRED)
# find_package(pybind11 REQUIRED)

# pybind11_add_module(
#     evaluate_module
#     main.cpp
#     liquidity.cpp
#     profitability.cpp
#     efficiency.cpp
#     growth.cpp
# )

# target_include_directories(evaluate_module PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
# target_link_libraries(evaluate_module PRIVATE pybind11::module Python3::Python)