cmake_minimum_required(VERSION 3.0.0)
project(libevt_svr_demo CXX)

set(CMAKE_CXX_COMPILER g++)

option(USE_O2 "Use -O2 instead of the default -O3" OFF)


# FILE(GLOB FBGEN "./gen-cpp2/*.cpp")
add_executable(echo_server
	echo_server.cpp
)

# find_package(Libevent REQUIRED)

target_link_libraries(echo_server PUBLIC        
    -levent
)
