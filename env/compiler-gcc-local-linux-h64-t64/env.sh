#! /bin/bash
# CK generated script

if [ "$1" != "1" ]; then if [ "$CK_ENV_COMPILER_GCC_SET" == "1" ]; then return; fi; fi

# Soft UOA         = compiler.gcc (3a8a82fa40bf992d) 
# Host OS UOA      = linux-64 (4258b5fe54828a50)
# Target OS UOA    = linux-64 (4258b5fe54828a50)
# Target OS bits   = 64
# Tool version     = local
# Tool int version = 88888

export CK_AR=ar
export CK_ASM_EXT=.s
export CK_CC=gcc
export CK_COMPILER_FLAGS_OBLIGATORY=
export CK_COMPILER_FLAG_CPP11=-std=c++11
export CK_COMPILER_FLAG_GPROF=-pg
export CK_COMPILER_FLAG_OPENMP=-fopenmp
export CK_COMPILER_FLAG_PLUGIN=-fplugin=
export CK_COMPILER_FLAG_PTHREAD_LIB=-lpthread
export CK_CXX=g++
export CK_DLL_EXT=.so
export CK_EXE_EXT=.out
export CK_EXTRA_LIB_DL=-ldl
export CK_EXTRA_LIB_M=-lm
export CK_F90=gfortran
export CK_F95=gfortran
export CK_FC=gfortran
export CK_FLAGS_CREATE_ASM=-S
export CK_FLAGS_CREATE_OBJ=-c
export CK_FLAGS_DLL="-shared -fPIC"
export CK_FLAGS_DLL_EXTRA=
export CK_FLAGS_OUTPUT="-o "
export CK_FLAGS_STATIC_BIN="-static -fPIC"
export CK_FLAGS_STATIC_LIB=-fPIC
export CK_FLAG_PREFIX_INCLUDE=-I
export CK_FLAG_PREFIX_LIB_DIR=-L
export CK_FLAG_PREFIX_VAR=-D
export CK_GPROF_OUT_FILE=gmon.out
export CK_LB="ar rcs"
export CK_LB_OUTPUT="-o "
export CK_LD=ld
export CK_LD_FLAGS_EXTRA=
export CK_LIB_EXT=.a
export CK_LINKER_FLAG_OPENMP="-lgomp -lrt"
export CK_MAKE=make
export CK_OBJDUMP="objdump -d"
export CK_OBJ_EXT=.o
export CK_OPT_SIZE=-Os
export CK_OPT_SPEED=-O3
export CK_OPT_SPEED_SAFE=-O2
export CK_PLUGIN_FLAG=-fplugin=
export CK_PROFILER=gprof

export CK_ENV_COMPILER_GCC_SET=1
