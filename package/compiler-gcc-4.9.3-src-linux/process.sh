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

export PACKAGE_NAME=gcc-4.9.3
export PACKAGE_FILE=${PACKAGE_NAME}.tar.bz2
export PACKAGE_URL=http://mirrors-uk.hotimportnights.com/gcc/releases/gcc-4.9.3/${PACKAGE_FILE}

cd ${INSTALL_DIR}

echo ""
echo "In the next step, we will download archive from ${PACKAGE_URL} ..."
echo "However, if you already have it, place it inside this directory:"
echo "${INSTALL_DIR}"
echo ""

read -p "Press [Enter] to continue ..."

if [ ! -f ${PACKAGE_FILE} ]; then

 echo ""
 echo "Downloading archive from ${PACKAGE_URL} ..."
 echo ""

 wget ${PACKAGE_URL}

 if [ "${?}" != "0" ] ; then
  echo "Error: Downloading failed in $PWD!" 
  exit 1
 fi
fi

echo ""
echo "Extracting archive ..."
echo ""

bzip2 -d ${PACKAGE_NAME}.tar.bz2
tar xvf ${PACKAGE_NAME}.tar
rm ${PACKAGE_NAME}.tar

if [ "${?}" != "0" ] ; then
 echo "Error: extraction failed in $PWD!" 
 exit 1
fi

export INSTALL_OBJ_DIR=${INSTALL_DIR}/obj
mkdir $INSTALL_OBJ_DIR

#
echo ""
echo "Configuring ..."

cd ${INSTALL_OBJ_DIR}
../${PACKAGE_NAME}/configure --prefix=${INSTALL_DIR} \
                             --enable-languages=c,c++,fortran \
                             --enable-shared \
                             --enable-static \
                             --enable-libgomp \
                             --enable-lto \
                             --enable-graphite

if [ "${?}" != "0" ] ; then
  echo "Error: Configuration failed in $PWD!"
  exit 1
fi

# Build
echo ""
echo "Building ..."
echo ""
cd ${INSTALL_OBJ_DIR}
make -j4
if [ "${?}" != "0" ] ; then
  echo "Error: Compilation failed in $PWD!" 
  exit 1
fi

# Install
echo ""
echo "Installing ..."
echo ""

make install
if [ "${?}" != "0" ] ; then
  echo "Error: Compilation failed in $PWD!" 
  exit 1
fi
