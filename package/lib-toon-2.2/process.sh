#! /bin/bash

#
# Installation script for CK packages.
#
# See CK LICENSE.txt for licensing details.
# See CK Copyright.txt for copyright details.
#
# Developer(s): Grigori Fursin, 2015
#

# PACKAGE_DIR
# INSTALL_DIR

export PACKAGE_NAME=TooN-2.2
export PACKAGE_NAME_ORIG=$PACKAGE_NAME

cd ${INSTALL_DIR}

mkdir include
cd include

cp ${PACKAGE_DIR}/${PACKAGE_NAME}.tar.bz2 .
bzip2 -d ${PACKAGE_NAME}.tar.bz2
tar xvf ${PACKAGE_NAME}.tar
rm ${PACKAGE_NAME}.tar


cd $PACKAGE_NAME
. ./configure
 if [ "${?}" != "0" ] ; then
  echo "Error: Compilation failed in $PWD!" 
  exit 1
 fi

cd ..
mv $PACKAGE_NAME_ORIG TooN
