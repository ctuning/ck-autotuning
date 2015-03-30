# Find cTuning (auto-tuning) plugin and set environment
ck set env tags=plugin,openme,ctuning bat_file=tmp-ck-env.sh --bat_new --print && . ./tmp-ck-env.sh && rm tmp-ck-env.sh || exit 1

export OPENME_USE=1
export OPENME_PLUGINS=${CK_ENV_PLUGIN_OPENME_CTUNING_LIB}/${CK_ENV_PLUGIN_OPENME_CTUNING_DYNAMIC_NAME}
export OPENME_OUTPUT_FILE=tmp-ck-plugin-output.json
export OPENME_DEBUG=1

ck run program
