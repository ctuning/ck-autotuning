Universal software and hardware autotuning
==========================================

Status
======
This is a relatively stable repository for universal,
multi-dimensional, multi-objective autotuning

Prerequisites
=============
* Collective Knowledge Framework: http://github.com/ctuning/ck

Description
===========
During many years of research on machine learning based autotuning 
we spent more time on data management then on innovation. At the end,
we decided to provide a complete solution in CK where our plugin-based 
autotuning tools are combined with our repository and python or
R-based machine learning plugins.

We are gradually moving, simplifying and extending autotuning
from Collective Mind into new CK format! Since design and optimization
spaces are very large, we are trying to make their exploration practical 
and scalable by combining autotuning, crowdsourcing, predictive 
analytics and run-time adaptation.

Modules from this repository will be used to unify:
* program compilation and execution (with multiple data sets)
* benchmarking
* statistical analysis
* plugin-based autotuning
* automatic performance modeling
* static and dynamic features extraction
* machine learning to predict optimizations and run-time adaptation
* reproducibility of experimental results

Publications
============
* http://hal.inria.fr/hal-01054763
* https://hal.inria.fr/inria-00436029
* http://arxiv.org/abs/1407.4075

Authors
=======

* Grigori Fursin, cTuning foundation (France) / dividiti (UK)

License
=======
* BSD, 3-clause

Installation
============

> ck pull repo:ck-autotuning

Modules with actions
====================

choice - exploring choices in multi-dimensional spaces (customizing autotuning)

  * make - make next choice in multi-dimensional space
  * select_list - select from a list of choices in console mode

compiler - describing compilers and their optimization choices

  * extract_to_pipeline - prepare compiler flag choices for universal tuning via program pipeline (experimental workflow)

dataset - datasets

dataset.features - dataset features

  * convert_raw_rgb_image - convert raw RGB image to png (originally used for SLAM application tuning)
  * extract - extract data set features

pipeline - defining universal pipelines (experiment workflows)

  * autotune - perform autotuning of any available CK pipeline (workflow)
  * run - run a given pipeline (workflow) once
  * run_stat - run a given pipeline (workflow) N times and perform statistical analysis
  * setup - setup a given pipeline (workflow) for execution/autotuning

pipeline.cmd - demonstrating command line pipeline (for CMD-based autotuning)

  * pipeline - run universal command line pipeline (demo)

program - program compilation and execution workflow (pipeline)

  * autotune - universal, multi-objective, multi-dimensional software/hardware autotuning
  * clean - clean temporal files and directories of a given program
  * compile - compile a given program
  * pipeline - universal program compilation and execution pipeline (workflow)
  * run - run a given program
  * select_uoa - select program UOA in console mode

program.experiment.speedup - checking program speedups vs compiler flags vs data sets

  * describe - describe experiment
  * reproduce - reproduce experiment

program.species - classification of similar programs using machine learning or manually by the community

program.static.features - program semantic features
