# Find cTuning (auto-tuning) plugin and set environment
call ck set env tags=plugin,openme,ctuning,target-os-windows-64 bat_file=tmp-ck-env.bat --bat_new --print && call tmp-ck-env.bat && del /Q tmp-ck-env.bat
if %errorlevel% neq 0 exit /b %errorlevel%

set OPENME_USE=1
set OPENME_PLUGINS=%CK_ENV_PLUGIN_OPENME_CTUNING_LIB%\%CK_ENV_PLUGIN_OPENME_CTUNING_DYNAMIC_NAME%
set OPENME_OUTPUT_FILE=tmp-ck-plugin-output.json
set OPENME_DEBUG=1

ck run program --skip_clean_after
