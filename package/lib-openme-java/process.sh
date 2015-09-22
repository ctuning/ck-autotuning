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

export LIB_NAME=libopenme

echo ""
echo "Obtaining latest OpenME from GitHub ..."
echo ""

cd ${INSTALL_DIR}

git clone https://github.com/ctuning/openme.git openme

cd openme
git pull

cd src/java

. ./ck-make.sh

if [ "${?}" != "0" ] ; then
  echo "Error: Compilation failed in $PWD!" 
  exit 1
fi
