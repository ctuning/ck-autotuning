#! /bin/bash

#
# Installation script for clBLAS.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2015;
# - Anton Lokhmotov, 2016.
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

############################################################
echo ""
echo "Cloning package from '${PACKAGE_URL}' ..."

rm -rf src

git clone ${PACKAGE_URL} src

if [ "${?}" != "0" ] ; then
  echo "Error: cloning package failed!"
  exit 1
fi

############################################################
echo ""
echo "Cleaning ..."

cd ${INSTALL_DIR}

rm -rf obj
mkdir obj
cd obj

############################################################
echo ""
echo "Executing cmake ..."

cmake -DCMAKE_INSTALL_PREFIX="${INSTALL_DIR}/install" \
      -Dprotobuf_BUILD_TESTS=OFF \
      ../src/cmake

if [ "${?}" != "0" ] ; then
  echo "Error: cmake failed!"
  exit 1
fi

############################################################
echo ""
echo "Building package ..."

rm -rf install

make -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS}
if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Installing package ..."

make install/strip
if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

exit 0
