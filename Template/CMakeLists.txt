cmake_minimum_required( VERSION 3.19 )
project( ModuleTemplate C )

set( PROJECT_NAME ModuleTemplate )

# set compiler settings
set( CMAKE_C_STANDARD 11 )
set( CMAKE_C_COMPILER x86_64-w64-mingw32-gcc )

# adding demon sources
include_directories( include )

set( COMMON_SOURCE
        src/Win32.c
        src/KaynLdr.c
        src/DllMain.c
        src/Parser.c
)


# add compiled demons
add_executable( ${PROJECT_NAME} ${COMMON_SOURCE} )
