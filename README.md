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
We are gradually moving, simplifying and extending autotuning
from Collective Mind into new CK format! Since design and optimization
spaces are very large, we are trying to make their exploration practical 
and scalable by combining autotuning, crowdsourcing, predictive 
analytics and run-time adaptation.

Modules from this repository will be used to:
* clean, compile and run programs 
* perform benchmarking
* perform plugin-based autotuning
* perform crowd-tuning
* perform statistical analysis
* gradually add reproducibility of results

Publications
============
* http://hal.inria.fr/hal-01054763
* https://hal.inria.fr/inria-00436029
* http://arxiv.org/abs/1407.4075
