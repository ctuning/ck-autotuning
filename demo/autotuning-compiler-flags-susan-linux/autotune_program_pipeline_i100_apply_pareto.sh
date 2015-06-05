ck cp experiment:demo-autotune-compiler-flags-susan-linux-i100 :demo-autotune-flags-susan-linux-pareto
ck autotune pipeline:program pipeline_from_file=_setup_program_pipeline_tmp.json @autotune_program_pipeline_i100_apply_pareto.json
