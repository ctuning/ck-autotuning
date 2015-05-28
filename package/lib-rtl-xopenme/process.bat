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

set LIB_NAME=libxopenme

echo.
echo Copying XOpenME to src dir ...
echo.

mkdir %INSTALL_DIR%\src

copy /B %PACKAGE_DIR%\xopenme.c %INSTALL_DIR%\src
copy /B %PACKAGE_DIR%\xopenme.h %INSTALL_DIR%\src
copy /B %PACKAGE_DIR%\ck-make.bat %INSTALL_DIR%\src
copy /B %PACKAGE_DIR%\README %INSTALL_DIR%\src

cd %INSTALL_DIR%\src

call ck-make.bat
if %errorlevel% neq 0 (
 echo.
 echo Problem building CK package!
 goto err
)

exit /b 0

:err
exit /b 1
