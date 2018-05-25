#
# Postprocessing CK template demo
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
#

import json
import os
import re
import sys

def ck_postprocess(i):

    ck=i['ck_kernel']
    rt=i['run_time']
    deps=i['deps']

    d={}

    env=i.get('env',{})

    return {'return':0}

# Check output with a reference one (can check numerical stability)

def ck_check_output(i):
    ck=i['ck_kernel']

    env=i.get('env',{})

    r=ck.access({'action':'check_numerical',
                 'module_uoa':'program.output',
                 'file1':i['file1'],
                 'file2':i['file2'],
                 'abs_threshold':env.get('CK_ABS_DIFF_THRESHOLD','')})
    return r

# Do not add anything here!

# Do not add anything here!
