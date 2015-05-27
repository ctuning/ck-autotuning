#! /bin/bash

#
# Make script for CK libraries
# (depends on configured/installed compilers via CK)
#
# See CK LICENSE.txt for licensing details.
# See CK Copyright.txt for copyright details.
#
# Developer(s): Grigori Fursin, 2015
#

echo ""
echo "Building static library ..."
echo ""

export CK_SOURCE_FILES="cJSON.c openme.c"
export CK_OBJ_FILES=cJSON${CK_OBJ_EXT} openme${CK_OBJ_EXT}

export CK_INCLUDE_FILE=openme.h
export CK_INCLUDE_FILE1=cJSON.h

export LIB_NAME=libopenme

export CK_COMPILER_FLAGS_MISC="${CK_FLAG_PREFIX_INCLUDE} . ${CK_COMPILER_FLAGS_MISC}"

export CK_TARGET_FILE=${LIB_NAME}${CK_LIB_EXT}
export CK_TARGET_FILE_S=${CK_TARGET_FILE}

export CK_CC_FLAGS="${CK_COMPILER_FLAGS_OBLIGATORY} ${CK_COMPILER_FLAGS_MISC} ${CK_COMPILER_FLAGS_CC_OPTS} ${CK_COMPILER_FLAGS_ARCH} ${CK_COMPILER_FLAGS_PAR}"

echo "Executing ${CK_CC} ${CK_FLAGS_STATIC_LIB} ${CK_FLAGS_CREATE_OBJ} ${CK_CC_FLAGS} ${CK_SOURCE_FILES} ${CK_LD_FLAGS_MISC} ${CK_LD_FLAGS_EXTRA}"
${CK_CC} ${CK_FLAGS_STATIC_LIB} ${CK_FLAGS_CREATE_OBJ} ${CK_CC_FLAGS} ${CK_SOURCE_FILES} ${CK_LD_FLAGS_MISC} ${CK_LD_FLAGS_EXTRA}
  if [ "${?}" != "0" ] ; then
    echo "Error: Compilation failed in $PWD!" 
    exit 1
  fi

echo "Executing ${CK_LB} ${CK_LB_OUTPUT}${CK_TARGET_FILE} ${CK_OBJ_FILES}"
${CK_LB} ${CK_LB_OUTPUT}${CK_TARGET_FILE} ${CK_OBJ_FILES}
  if [ "${?}" != "0" ] ; then
    echo "Error: Compilation failed in $PWD!" 
    exit 1
  fi

echo ""
echo "Building dynamic library ..."
echo ""

export CK_TARGET_FILE=${LIB_NAME}${CK_DLL_EXT}
export CK_TARGET_FILE_D=${CK_TARGET_FILE}

export CK_CC_FLAGS="${CK_COMPILER_FLAGS_OBLIGATORY} ${CK_COMPILER_FLAGS_MISC} ${CK_COMPILER_FLAGS_CC_OPTS} ${CK_COMPILER_FLAGS_ARCH} ${CK_COMPILER_FLAGS_PAR}"

echo "Executing ${CK_CC} ${CK_FLAGS_DLL} ${CK_CC_FLAGS} ${CK_SOURCE_FILES} ${CK_FLAGS_OUTPUT}${CK_TARGET_FILE} ${CK_FLAGS_DLL_EXTRA} ${CK_LD_FLAGS_MISC} ${CK_LD_FLAGS_EXTRA}"
${CK_CC} ${CK_FLAGS_DLL} ${CK_CC_FLAGS} ${CK_SOURCE_FILES} ${CK_FLAGS_OUTPUT}${CK_TARGET_FILE} ${CK_FLAGS_DLL_EXTRA} ${CK_LD_FLAGS_MISC} ${CK_LD_FLAGS_EXTRA}
  if [ "${?}" != "0" ] ; then
    echo "Error: Compilation failed in $PWD!" 
    exit 1
  fi

echo ""
echo "Installing ..."
echo ""

mkdir ${INSTALL_DIR}/lib
cp -f ${CK_TARGET_FILE_S} ${INSTALL_DIR}/lib
cp -f ${CK_TARGET_FILE_D} ${INSTALL_DIR}/lib

mkdir ${INSTALL_DIR}/include
cp ${CK_INCLUDE_FILE} ${INSTALL_DIR}/include
cp ${CK_INCLUDE_FILE1} ${INSTALL_DIR}/include
