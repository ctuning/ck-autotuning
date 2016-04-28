rem  Find cTuning (auto-tuning) plugin and set environment
call ck set env tags=plugin,openme,ctuning,target-os-android19-arm bat_file=tmp-ck-env.bat --bat_new --print && call tmp-ck-env.bat && del /Q tmp-ck-env.bat
if %errorlevel% neq 0 exit /b %errorlevel%

echo Copying plugin to remote device ...
adb push %CK_ENV_PLUGIN_OPENME_CTUNING_LIB%\%CK_ENV_PLUGIN_OPENME_CTUNING_DYNAMIC_NAME% /data/local/tmp

ck run program target_os=android19-arm --console extra_env="export OPENME_USE=1; export OPENME_PLUGINS=/data/local/tmp/%CK_ENV_PLUGIN_OPENME_CTUNING_DYNAMIC_NAME%; export OPENME_OUTPUT_FILE=tmp-ck-plugin-output.json; export OPENME_DEBUG=1" --skip_clean_after
