Universal, customizable and multi-objective software and hardware autotuning
============================================================================

**All CK components can be found at [cKnowledge.io](https://cKnowledge.io) and in [one GitHub repository](https://github.com/ctuning/ck-mlops)!**

*This project is hosted by the [cTuning foundation](https://cTuning.org).*

[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Linux & MacOS: [![Travis Build Status](https://travis-ci.org/ctuning/ck-autotuning.svg?branch=master)](https://travis-ci.org/ctuning/ck-autotuning)
Windows: [![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/github/ctuning/ck-autotuning?branch=master&svg=true)](https://ci.appveyor.com/project/ens-lg4/ck-autotuning)

This is a [CK repository](https://github.com/ctuning/ck) for the universal, customizable, 
multi-dimensional and multi-objective SW/HW benchmarking, autotuning 
and co-design with a unified JSON API across Linux, Android, MacOS 
and Windows-based machines.

![logo](https://github.com/ctuning/ck-guide-images/blob/master/image-pipelines2.png)

This repository included CK modules, actions and components for unified

* program compilation and execution (with multiple data sets)
* crowd-benchmarking
* statistical analysis of empirical results
* plugin-based autotuning
* automatic performance modeling
* static and dynamic features extraction
* learning to predict optimizations and run-time adaptation
* reproducibility of experimental results

Further info:
* [Shared portable CK program workflows](https://cKnowledge.io/programs)
* [Open CK platform to publish and download stable CK components](https://cKnowledge.io/docs)
* [MLPerf crowd-benchmarking demo](https://cknowledge.io/demo)
* [Documentation about portable CK workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
* [Related CK publications](https://github.com/ctuning/ck/wiki/Publications)

Author
======
* [Grigori Fursin](https://fursin.net)

Contributors
============
* See the list of [contributors](https://github.com/ctuning/ck-autotuning/blob/master/CONTRIBUTIONS)

Shared CK modules with actions
==============================

* [program](https://cKnowledge.io/c/module/program)
* [program.output](https://cKnowledge.io/c/module/program.output)
* [pipeline](https://cKnowledge.io/c/module/pipeline)
* [pipeline.cmd](https://cKnowledge.io/c/module/pipeline.cmd)
* [platform.gpgpu](https://cKnowledge.io/c/module/platform.gpgpu)
* [algorithm](https://cKnowledge.io/c/module/algorithm)
* [choice](https://cKnowledge.io/c/module/choice)
* [compiler](https://cKnowledge.io/c/module/compiler)
* [dataset](https://cKnowledge.io/c/module/dataset)
* [dataset.features](https://cKnowledge.io/c/module/dataset.features)
* [program.behavior](https://cKnowledge.io/c/module/program.behavior)
* [program.dynamic.features](https://cKnowledge.io/c/module/program.dynamic.features)
* [program.experiment.speedup](https://cKnowledge.io/c/module/program.experiment.speedup)
* [program.species](https://cKnowledge.io/c/module/program.species)
* [program.static.features](https://cKnowledge.io/c/module/program.static.features)

Installation
============

First install the CK framework as described [here](https://github.com/ctuning/ck#installation).

Then install this CK repository as follows:

```
 $ ck pull repo:ck-autotuning

```

You can now browse and reuse program workflows shared at the [CK portal](https://cKnowledge.io/programs).

Please refer to the [CK online guides](https://github.com/ctuning/ck/wiki)
including [CK portable workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
and the [autotuning example](https://github.com/ctuning/ck/wiki/Autotuning).

Troubleshooting
===============
* Issues with GLIBCXX_3.4.20/3.4.21 when using LLVM installed via CK: These sometimes occur on earlier Ubuntu versions (14.04) 
  on ARM/x86. This can be fixed by upgrading to later versions of Ubuntu, or can sometimes be fixed by:

```
 $ sudo add-apt-repository ppa:ubuntu-toolchain-r/test
 $ sudo apt-get update
 $ sudo apt-get upgrade
 $ sudo apt-get dist-upgrade
```

* Issues with libncursesw.so.6 (not found) on some older machines: It can be fixed 
  by compiling and installing lib-ncurses with the support for wide characters. This can be done automatically via CK:

```
 $ ck install package:lib-ncurses-6.0-root
```

Questions and comments
======================

Please feel free to get in touch with the [CK community](https://github.com/ctuning/ck/wiki/Contacts) 
if you have any questions, suggestions and comments!
