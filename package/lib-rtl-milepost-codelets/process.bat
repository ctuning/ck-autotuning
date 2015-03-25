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

set PACKAGE_NAME=lib-rtl-milepost-codelet
set LIB_NAME=librtlmilepostcodelet

echo.
echo Extracting archive ...
echo.

cd %INSTALL_DIR%
copy /B %PACKAGE_DIR%\%PACKAGE_NAME%.tar.bz2 .
bzip2 -d %PACKAGE_NAME%.tar.bz2
tar xvf %PACKAGE_NAME%.tar
del /Q %PACKAGE_NAME%.tar

if %errorlevel% neq 0 (
 echo.
 echo Failed extracting package archive!
 goto err
)

cd src

call ck-make.bat
if %errorlevel% neq 0 (
 echo.
 echo Problem building CK package!
 goto err
)

exit /b 0

:err
exit /b 1
