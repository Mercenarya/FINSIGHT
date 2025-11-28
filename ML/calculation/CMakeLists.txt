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

# Last module processing (Định nghĩa target)
pybind11_add_module(evaluate_module_update ${SOURCES})

# Thêm lệnh Find Python (Dùng cho target)
find_package(Python 3.11 COMPONENTS Interpreter Development)

# Thêm thư viện Python vào target (Đã sửa tên target)
target_link_libraries(evaluate_module_update PRIVATE ${PYTHON_LIBRARIES})

# **QUAN TRỌNG:** Buộc MinGW sử dụng thư viện Python đúng cách (Đã sửa tên target)
target_link_options(evaluate_module_update PRIVATE
    "-Wl,--allow-multiple-definition"
)
