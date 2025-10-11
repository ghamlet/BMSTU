cmake_minimum_required(VERSION 3.16)

project(prnod LANGUAGES C)

add_executable(prnod main.c
    Nod.c
    Nod.h)

include(GNUInstallDirs)
install(TARGETS prnod
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
