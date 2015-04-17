Status
======
This is an unstable, heavily evolving repository 
(stable release is expected in Spring 2015) - 
please, do not use it until official announcement.

Dependencies
============
* CK repo: ck-env (to install, interconnect and call various tools and their version)
* CK repo: ck-analytics (to record experiments and expose to predictive analytics)

> ck add repo:ck-env --shared --quiet
> ck add repo:ck-analytics --shared --quiet

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
* crowd-tuning
* reproducibility of experimental results

Publications
============
* http://hal.inria.fr/hal-01054763
* https://hal.inria.fr/inria-00436029
* http://arxiv.org/abs/1407.4075
