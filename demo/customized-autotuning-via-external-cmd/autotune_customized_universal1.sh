#! /bin/bash

export CK_CUR_PATH=$PWD
export CK_CUSTOM_AUTOTUNER_SCRIPT="${CK_CUR_PATH}/autotune_customized_universal1_plugin.sh"

ck autotune program:custom-autotuning-wrapper @autotune_customized_universal1.json --new --skip_collaborative --skip_pruning --scenario=experiment.tune.custom.dimensions
