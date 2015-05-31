@echo off

rem CK generated script

if not [%1] == [1] (if defined CK_ENV_COMPILER_GCC_SET exit /b 0)

rem Soft UOA         = compiler.gcc (3a8a82fa40bf992d) 
rem Host OS UOA      = windows-64 (7a95e0754c37610a)
rem Target OS UOA    = mingw-32 (d4c3a9e4a9a77677)
rem Target OS bits   = 32
rem Tool version     = local
rem Tool int version = 88888

set CK_AR=ar
set CK_ASM_EXT=.s
set CK_CC=gcc
set CK_COMPILER_FLAGS_OBLIGATORY= -DWINDOWS
set CK_COMPILER_FLAG_CPP11=-std=c++11
set CK_COMPILER_FLAG_GPROF=-pg
set CK_COMPILER_FLAG_OPENMP=-fopenmp
set CK_COMPILER_FLAG_PLUGIN=-fplugin=
set CK_COMPILER_FLAG_PTHREAD_LIB=-lpthread
set CK_CXX=g++ -fpermissive
set CK_DLL_EXT=.so
set CK_EXE_EXT=.out
set CK_EXTRA_LIB_DL=-ldl
set CK_EXTRA_LIB_M=-lm
set CK_F90=gfortran
set CK_F95=gfortran
set CK_FC=gfortran
set CK_FLAGS_CREATE_ASM=-S
set CK_FLAGS_CREATE_OBJ=-c
set CK_FLAGS_DLL=-shared -fPIC
set CK_FLAGS_DLL_EXTRA=
set CK_FLAGS_OUTPUT=-o 
set CK_FLAGS_STATIC_BIN=-static -fPIC
set CK_FLAGS_STATIC_LIB=-fPIC
set CK_FLAG_PREFIX_INCLUDE=-I
set CK_FLAG_PREFIX_LIB_DIR=-L
set CK_FLAG_PREFIX_VAR=-D
set CK_GPROF_OUT_FILE=gmon.out
set CK_LB=ar rcs
set CK_LB_OUTPUT=-o 
set CK_LD=ld
set CK_LD_FLAGS_EXTRA=
set CK_LIB_EXT=.a
set CK_LINKER_FLAG_OPENMP=-lgomp -lrt
set CK_MAKE=mingw32-make
set CK_OBJDUMP=objdump -d
set CK_OBJ_EXT=.o
set CK_OPT_SIZE=-Os
set CK_OPT_SPEED=-O3
set CK_OPT_SPEED_SAFE=-O2
set CK_PLUGIN_FLAG=-fplugin=
set CK_PROFILER=gprof

set CK_ENV_COMPILER_GCC_SET=1

exit /b 0
