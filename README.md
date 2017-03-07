Universal, customizable and multi-objective software and hardware autotuning
============================================================================

This is a stable repository for universal, customizable, 
multi-dimensional, multi-objective SW/HW autotuning 
with JSON API across Linux, Android, MacOS and Windows-based machines
using [Collective Knowledge Framework](https://github.com/ctuning/ck).

![logo](https://github.com/ctuning/ck-guide-images/blob/master/image-pipelines2.png)

Please, check out examples in this [demo directory](https://github.com/ctuning/ck-autotuning/tree/master/demo)
and notes about [CK portable and customizable workflows](https://github.com/ctuning/ck/wiki/Portable-workflows).

These reusable and customizable modules are now used in various common 
experimental scenarios include universal,
customizable, multi-dimensional, multi-objective 
[DNN crowd-benchmarking](http://cKnowledge.org/ai) 
and [compiler crowd-tuning](http://github.com/ctuning/ck-autotuning).

See continuously aggregated public results results and
unexpected behavior in the [CK live repository](http://cKnowledge.org/repo)!

Also check out our related Android apps to let you participate in our experiment crowdsourcing using
spare Android mobile phones, tables and other devices:
* [collaborative deep learning optimization app](https://github.com/dividiti/crowdsource-video-experiments-on-android)
* [compiler tuning using small kernels](https://play.google.com/store/apps/details?id=openscience.crowdsource.experiments)
* [CK crowd-scenarios](https://github.com/ctuning/ck-crowd-scenarios)

Further details are available at [CK wiki](https://github.com/ctuning/ck/wiki)
and our [open research challenges](https://github.com/ctuning/ck/wiki/Enabling-open-science).

Prerequisites
=============
* [Collective Knowledge Framework](http://github.com/ctuning/ck)

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

Authors
=======

* [Grigori Fursin](http://fursin.net/research.html), dividiti/cTuning foundation
* [Anton Lokhmotov](https://www.hipeac.net/~anton), dividiti (UK)

License
=======
* BSD, 3-clause

Installation
============

> ck pull repo:ck-autotuning

Usage
=====

Please, refer to the [CK online guides](https://github.com/ctuning/ck/wiki)
including [CK portable workflows](https://github.com/ctuning/ck/wiki/Portable-workflows)
and [autotuning example](https://github.com/ctuning/ck/wiki/Autotuning).

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

Publications
============

The concepts have been described in the following publications:

```
@article{fursin:hal-01054763,
    hal_id = {hal-01054763},
    url = {http://hal.inria.fr/hal-01054763},
    title = {{Collective Mind}: Towards practical and collaborative auto-tuning},
    author = {Fursin, Grigori and Miceli, Renato and Lokhmotov, Anton and Gerndt, Michael and Baboulin, Marc and Malony, Allen, D. and Chamski, Zbigniew and Novillo, Diego and Vento, Davide Del},
    abstract = {{Empirical auto-tuning and machine learning techniques have been showing high potential to improve execution time, power consumption, code size, reliability and other important metrics of various applications for more than two decades. However, they are still far from widespread production use due to lack of native support for auto-tuning in an ever changing and complex software and hardware stack, large and multi-dimensional optimization spaces, excessively long exploration times, and lack of unified mechanisms for preserving and sharing of optimization knowledge and research material. We present a possible collaborative approach to solve above problems using Collective Mind knowledge management system. In contrast with previous cTuning framework, this modular infrastructure allows to preserve and share through the Internet the whole auto-tuning setups with all related artifacts and their software and hardware dependencies besides just performance data. It also allows to gradually structure, systematize and describe all available research material including tools, benchmarks, data sets, search strategies and machine learning models. Researchers can take advantage of shared components and data with extensible meta-description to quickly and collaboratively validate and improve existing auto-tuning and benchmarking techniques or prototype new ones. The community can now gradually learn and improve complex behavior of all existing computer systems while exposing behavior anomalies or model mispredictions to an interdisciplinary community in a reproducible way for further analysis. We present several practical, collaborative and model-driven auto-tuning scenarios. We also decided to release all material at http://c-mind.org/repo to set up an example for a collaborative and reproducible research as well as our new publication model in computer engineering where experimental results are continuously shared and validated by the community.}},
    keywords = {High performance computing; systematic auto-tuning; systematic benchmarking; big data driven optimization; modeling of computer behavior; performance prediction; predictive analytics; feature selection; collaborative knowledge management; NoSQL repository; code and data sharing; specification sharing; collaborative experimentation; machine learning; data mining; multi-objective optimization; model driven optimization; agile development; plugin-based auto-tuning; performance tracking buildbot; performance regression buildbot; performance tuning buildbot; open access publication model; collective intelligence; reproducible research},
    language = {Anglais},
    affiliation = {POSTALE - INRIA Saclay - Ile de France , cTuning foundation , University of Rennes 1 , ICHEC , ARM [Cambridge] , Technical University of Munich - TUM , Computer Science Department [Oregon] , Infrasoft IT Solutions , Google Inc , National Center for Atmospheric Research - NCAR},
    booktitle = {{Automatic Application Tuning for HPC Architectures}},
    publisher = {IOS Press},
    pages = {309-329},
    journal = {Scientific Programming},
    volume = {22},
    number = {4 },
    audience = {internationale },
    doi = {10.3233/SPR-140396 },
    year = {2014},
    month = Jul,
    pdf = {http://hal.inria.fr/hal-01054763/PDF/paper.pdf},
}

@inproceedings{ck-date16,
    title = {{Collective Knowledge}: towards {R\&D} sustainability},
    author = {Fursin, Grigori and Lokhmotov, Anton and Plowman, Ed},
    booktitle = {Proceedings of the Conference on Design, Automation and Test in Europe (DATE'16)},
    year = {2016},
    month = {March},
    url = {https://www.researchgate.net/publication/304010295_Collective_Knowledge_Towards_RD_Sustainability}
}

@inproceedings{Fur2009,
  author =    {Grigori Fursin},
  title =     {{Collective Tuning Initiative}: automating and accelerating development and optimization of computing systems},
  booktitle = {Proceedings of the GCC Developers' Summit},
  year =      {2009},
  month =     {June},
  location =  {Montreal, Canada},
  keys =      {http://www.gccsummit.org/2009}
  url  =      {https://scholar.google.com/citations?view_op=view_citation&hl=en&user=IwcnpkwAAAAJ&cstart=20&citation_for_view=IwcnpkwAAAAJ:8k81kl-MbHgC}
}
```

* http://arxiv.org/abs/1506.06256
* http://hal.inria.fr/hal-01054763
* https://hal.inria.fr/inria-00436029
* http://arxiv.org/abs/1407.4075
* https://scholar.google.com/citations?view_op=view_citation&hl=en&user=IwcnpkwAAAAJ&citation_for_view=IwcnpkwAAAAJ:LkGwnXOMwfcC

Feedback
========

If you have problems, questions or suggestions, do not hesitate to get in touch
via the following mailing lists:
* https://groups.google.com/forum/#!forum/collective-knowledge
* https://groups.google.com/forum/#!forum/ctuning-discussions

