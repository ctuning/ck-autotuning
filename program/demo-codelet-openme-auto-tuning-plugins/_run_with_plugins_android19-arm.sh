# Find cTuning (auto-tuning) plugin and set environment
ck set env tags=plugin,openme,ctuning,target-os-android-32 bat_file=tmp-ck-env.sh --bat_new --print && . ./tmp-ck-env.sh && rm tmp-ck-env.sh || exit 1

echo "Copying plugin to remote device ..."
adb push ${CK_ENV_PLUGIN_OPENME_CTUNING_LIB}/${CK_ENV_PLUGIN_OPENME_CTUNING_DYNAMIC_NAME} /data/local/tmp

ck run program target_os=android5-arm --console extra_env="export OPENME_USE=1; export OPENME_PLUGINS=./${CK_ENV_PLUGIN_OPENME_CTUNING_DYNAMIC_NAME}; export OPENME_OUTPUT_FILE=tmp-ck-plugin-output.json; export OPENME_DEBUG=1" --skip_clean_after
