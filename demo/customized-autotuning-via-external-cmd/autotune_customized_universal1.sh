#! /bin/bash

export CK_CUR_PATH=`dirname $0`
export CK_CUSTOM_AUTOTUNER_SCRIPT="${CK_CUR_PATH}/autotune_customized_universal1_plugin.sh"

ck autotune program:custom-autotuning-wrapper @autotune_customized_universal1.json --new --skip_collaborative --scenario=experiment.tune.custom.dimensions
