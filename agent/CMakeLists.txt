cmake_minimum_required(VERSION 3.21)
project(bibliotheque)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Sources de la logique (tout sauf main.cpp et bindings.cpp)
set(CORE_SOURCES
    book.cpp
    user.cpp
    library.cpp
    filemanager.cpp
)

# Bibliothèque statique commune
add_library(core STATIC ${CORE_SOURCES})
set_target_properties(core PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
    POSITION_INDEPENDENT_CODE ON
)
target_compile_options(core PRIVATE -Wall -Wextra -Wpedantic)
target_include_directories(core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Exécutable console
add_executable(${PROJECT_NAME} main.cpp)
set_target_properties(${PROJECT_NAME} PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
)
target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic)
target_link_libraries(${PROJECT_NAME} PRIVATE core)

# Module Python (seulement si bindings.cpp existe)
option(BUILD_PYTHON_BINDINGS "Construire le module Python pybind11" ON)

if(BUILD_PYTHON_BINDINGS AND EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/bindings.cpp)
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin/python")
        if(NOT DEFINED PYTHON_EXECUTABLE)
            set(PYTHON_EXECUTABLE "${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin/python" CACHE FILEPATH "Interpréteur Python pour pybind11")
        endif()
        if(NOT DEFINED pybind11_DIR)
            execute_process(
                COMMAND "${PYTHON_EXECUTABLE}" -m pybind11 --cmakedir
                OUTPUT_VARIABLE _pybind11_cmake_dir
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
            )
            if(_pybind11_cmake_dir)
                set(pybind11_DIR "${_pybind11_cmake_dir}" CACHE PATH "Répertoire CMake de pybind11")
            endif()
        endif()
    endif()
    find_package(pybind11 CONFIG REQUIRED)
    pybind11_add_module(bibliotheque_py bindings.cpp)
    set_target_properties(bibliotheque_py PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO
    )
    target_compile_options(bibliotheque_py PRIVATE -Wall -Wextra -Wpedantic)
    target_link_libraries(bibliotheque_py PRIVATE core)
endif()
