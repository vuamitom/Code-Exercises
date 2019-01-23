cmake_minimum_required(VERSION 3.0.0)
project(test_client CXX)

set(CMAKE_CXX_COMPILER g++)

macro(remove_cxx_flag flag)
    string(REPLACE "${flag}" "" CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE}")
endmacro()

option(USE_O2 "Use -O2 instead of the default -O3" OFF)

# set(THREADS_PREFER_PTHREAD_FLAG ON)

FILE(GLOB FBGEN "../gen-cpp2/*.cpp")
add_executable(test_client
	test_future.cc	
    ${FBGEN}
)

find_package(FBThrift REQUIRED)
find_package(Folly REQUIRED)
find_package(Wangle REQUIRED)
find_package(fizz REQUIRED)
find_package(Threads REQUIRED)

target_link_libraries(test_client PUBLIC        
    FBThrift::thriftcpp2
)
