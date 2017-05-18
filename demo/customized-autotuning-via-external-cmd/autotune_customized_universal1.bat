@echo off

set CK_CUR_PATH=%~dp0
set CK_CUSTOM_AUTOTUNER_SCRIPT="%CK_CUR_PATH%\autotune_customized_universal1_plugin.bat"

ck autotune program:custom-autotuning-wrapper @autotune_customized_universal1.json --new --skip_collaborative --skip_pruning --scenario=experiment.tune.custom.dimensions
