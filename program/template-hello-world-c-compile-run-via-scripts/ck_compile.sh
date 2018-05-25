#!/bin/bash

echo "$CK_CC $CK_FLAGS_CREATE_OBJ $CK_COMPILER_FLAGS_OBLIGATORY $CK_FLAGS_DYNAMIC_BIN ${CK_FLAG_PREFIX_INCLUDE}../ ${CK_FLAG_PREFIX_VAR}CK_HOST_OS_NAME2_LINUX=1 ${CK_FLAG_PREFIX_VAR}CK_HOST_OS_NAME_LINUX=1 ${CK_FLAG_PREFIX_VAR}CK_TARGET_OS_NAME2_LINUX=1 ${CK_FLAG_PREFIX_VAR}CK_TARGET_OS_NAME_LINUX=1  ../hello-world.c  ${CK_FLAGS_OUTPUT}hello-world.o"
$CK_CC $CK_FLAGS_CREATE_OBJ $CK_COMPILER_FLAGS_OBLIGATORY $CK_FLAGS_DYNAMIC_BIN ${CK_FLAG_PREFIX_INCLUDE}../ ${CK_FLAG_PREFIX_VAR}CK_HOST_OS_NAME2_LINUX=1 ${CK_FLAG_PREFIX_VAR}CK_HOST_OS_NAME_LINUX=1 ${CK_FLAG_PREFIX_VAR}CK_TARGET_OS_NAME2_LINUX=1 ${CK_FLAG_PREFIX_VAR}CK_TARGET_OS_NAME_LINUX=1  ../hello-world.c  ${CK_FLAGS_OUTPUT}hello-world.o
er=$?; if [ $er != 0 ]; then exit $er; fi

echo "$CK_CC $CK_COMPILER_FLAGS_OBLIGATORY  $CK_FLAGS_DYNAMIC_BIN hello-world.o  ${CK_FLAGS_OUTPUT}a.out $CK_LD_FLAGS_MISC $CK_LD_FLAGS_EXTRA $CK_EXTRA_LIB_M"
$CK_CC $CK_COMPILER_FLAGS_OBLIGATORY  $CK_FLAGS_DYNAMIC_BIN hello-world.o  ${CK_FLAGS_OUTPUT}a.out $CK_LD_FLAGS_MISC $CK_LD_FLAGS_EXTRA $CK_EXTRA_LIB_M
er=$?; if [ $er != 0 ]; then exit $er; fi

$CK_OBJDUMP a.out > a.out.dump

md5sum < a.out.dump > a.out.md5

git rev-parse HEAD > a.out.git_hash 2>null

exit 0