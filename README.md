Universal, customizable and multi-objective software and hardware autotuning
============================================================================

Status
======
This is a stable repository for universal, customizable, 
multi-dimensional, multi-objective SW/HW autotuning 
across Linux, Android, MacOS and Windows-based machines
via Collective Knowledge Framework.

See related [Android app](https://play.google.com/store/apps/details?id=openscience.crowdsource.experiments)
to let you participate in GCC/LLVM crowd-tuning using
spare Android mobile phones, tables and other devices.

Further details are available at [CK wiki](https://github.com/ctuning/ck/wiki).

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

Please, check out [CK Getting Started Guide](https://github.com/ctuning/ck/wiki) for more details!

Publications
============
* http://hal.inria.fr/hal-01054763
* http://arxiv.org/abs/1506.06256
* http://bit.ly/ck-date16
* https://hal.inria.fr/inria-00436029
* http://arxiv.org/abs/1407.4075

Authors
=======

* Grigori Fursin, cTuning foundation (France) / dividiti (UK)
* Anton Lokhmotov, dividiti (UK)

License
=======
* BSD, 3-clause

Installation
============

> ck pull repo:ck-autotuning


Usage
=====

Please, refer to our [online guide](https://github.com/ctuning/ck/wiki)!

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

