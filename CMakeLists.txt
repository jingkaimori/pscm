cmake_minimum_required(VERSION 3.22)
project(pscm VERSION 0.2.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# https://cmake.org/cmake/help/latest/module/FindICU.html#module:FindICU
# find_package(ICU REQUIRED) is broken on MacOS due to Failed to find all ICU components
# TODO: better way to handle icu4c
if (NOT DEFINED ICU4C_ROOT)
  message(FATAL_ERROR "use cmake -DICU4C_ROOT=/path/to/your/icu4c")
endif()
function(_import_icu_ component)
if(NOT TARGET ICU::${component})
add_library(ICU::${component} UNKNOWN IMPORTED)
find_library(ICU_${component}_LIBRARY NAMES icu${component} HINTS ${ICU4C_ROOT}/lib)
if (ICU_${component}_LIBRARY)
message(STATUS "ICU_${component}_LIBRARY: ${ICU_${component}_LIBRARY}")
set_target_properties(ICU::${component} PROPERTIES
          INTERFACE_INCLUDE_DIRECTORIES "${ICU4C_ROOT}/include"
          INTERFACE_LINK_DIRECTORIES "${ICU4C_ROOT}/lib"
          INTERFACE_LINK_LIBRARIES ${ICU_${component}_LIBRARY}
          IMPORTED_LOCATION "${ICU_${component}_LIBRARY}"
          )
          message(INFO "Imported ICU::${component}")
else()
  message(WARNING "icu${component} not found")
endif()
endif()
endfunction(_import_icu_)
_import_icu_(uc)
_import_icu_(i18n)
_import_icu_(io)
find_package(Git REQUIRED)
message(STATUS "Git: ${GIT_EXECUTABLE}")
set(GIT_HASH "unknown")
set(GIT_BRANCH "unknown")
execute_process(
        COMMAND ${GIT_EXECUTABLE} log -1 --pretty=format:%H
        OUTPUT_VARIABLE GIT_HASH
        OUTPUT_STRIP_TRAILING_WHITESPACE
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}

)
execute_process(
        COMMAND ${GIT_EXECUTABLE} symbolic-ref --short -q HEAD
        OUTPUT_VARIABLE GIT_BRANCH
        OUTPUT_STRIP_TRAILING_WHITESPACE
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
message(STATUS "GIT_BRANCH: ${GIT_BRANCH}")
message(STATUS "GIT_HASH: ${GIT_HASH}")
configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/include/pscm/version.h.in
        ${CMAKE_CURRENT_BINARY_DIR}/generate/pscm/version.h
        @ONLY
)
add_subdirectory(3rd)
add_library(pscm)
target_include_directories(pscm PUBLIC include)
target_include_directories(pscm PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/generate)
aux_source_directory(src PSCM_SRCS)
target_sources(pscm PRIVATE ${PSCM_SRCS})
target_link_libraries(pscm PUBLIC spdlog::spdlog)
if (EMSCRIPTEN)
    target_compile_definitions(pscm PUBLIC WASM_PLATFORM)
    target_link_options(pscm PUBLIC "-sEXPORTED_RUNTIME_METHODS=ccall,cwrap")
    target_link_options(pscm PUBLIC "-sNO_DISABLE_EXCEPTION_CATCHING")
    add_subdirectory(wasm)
else ()
    add_executable(pscm_main main.cpp)
    target_link_libraries(pscm_main PRIVATE pscm)
endif ()
add_subdirectory(test)
add_subdirectory(example)
add_subdirectory(tool)
