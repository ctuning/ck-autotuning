@echo off

rem
rem Installation script for CK packages.
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, 2015
rem

rem PACKAGE_DIR
rem INSTALL_DIR

set PACKAGE_NAME=TooN-2.2
set PACKAGE_NAME_ORIG=%PACKAGE_NAME%

echo.
echo Extracting archive ...
echo.

cd %INSTALL_DIR%

mkdir include
cd include

copy /B %PACKAGE_DIR%\%PACKAGE_NAME%.tar.bz2 .
bzip2 -d %PACKAGE_NAME%.tar.bz2
tar xvf %PACKAGE_NAME%.tar
del /Q %PACKAGE_NAME%.tar

if %errorlevel% neq 0 (
 echo.
 echo Failed extracting package archive!
 goto err
)

cd ..
ren %PACKAGE_NAME_ORIG% TooN

exit /b 0

:err
exit /b 1
