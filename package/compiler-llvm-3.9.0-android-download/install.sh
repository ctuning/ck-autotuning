#! /bin/bash

#
# Installation script for LLVM.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2015
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

############################################################
# Check which file to download

if [ "${CK_ANDROID_ABI}" == "arm64-v8a" ] ; then
  PACKAGE_FILE=${PACKAGE_FILE_ARM64}
elif [ "${CK_ANDROID_ABI}" == "armeabi" ] ; then
  PACKAGE_FILE=${PACKAGE_FILE_ARMV7A}
else
  echo "CK Android ABI ${CK_ANDROID_ABI} is not supported!"
  exit 1
fi

URL=${PACKAGE_URL}/${PACKAGE_VERSION}/${PACKAGE_FILE}

############################################################
echo ""
echo "Downloading package from '${URL}' ..."

rm -f ${PACKAGE_FILE}
wget ${URL}
if [ "${?}" != "0" ] ; then
  echo "Error: downloading failed!"
  exit 1
fi

############################################################
echo ""
echo "Untarring and unzipping ..."

tar xvf ${PACKAGE_FILE} --strip 1
if [ "${?}" != "0" ] ; then
  echo "Error: untarring failed!"
  exit 1
fi

exit 0
