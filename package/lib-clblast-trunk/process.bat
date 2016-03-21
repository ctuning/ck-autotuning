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

set LIB_NAME=libclblast

echo.
echo Obtaining latest CLBlast from GitHub ...
echo.

cd %INSTALL_DIR%

git clone https://github.com/CNugteren/CLBlast clblast

cd clblast
git pull

md build
cd build

cmake.exe -DCMAKE_C_COMPILER=d:\Work1\CK\ck-tools\llvm-3.6-x86\bin\clang.exe -DCMAKE_CXX_COMPILER=d:\Work1\CK\ck-tools\llvm-3.6-x86\bin\clang.exe -DCMAKE_INSTALL_PREFIX=%INSTALL_DIR% ..
if %errorlevel% neq 0 (
 echo.
 echo Problem building CK package!
 goto err
)

echo.
echo Building using Visual Studio ...

msbuild.exe INSTALL.vcxproj > xyz 2> xyz1
if %errorlevel% neq 0 (
 echo.
 echo Problem building CK package!
 goto err
)

exit /b 0

:err
exit /b 1
