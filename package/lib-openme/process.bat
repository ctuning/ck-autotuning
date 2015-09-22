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

set LIB_NAME=libopenme

echo.
echo Obtaining latest OpenME from GitHub ...
echo.

cd %INSTALL_DIR%

git clone https://github.com/ctuning/openme.git openme

cd openme
git pull

cd src\c

call ck-make.bat
if %errorlevel% neq 0 (
 echo.
 echo Problem building CK package!
 goto err
)

exit /b 0

:err
exit /b 1
