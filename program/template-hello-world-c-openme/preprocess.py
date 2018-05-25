#
# Preprocessing CK template demo
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
#

import json
import os
import re

def ck_preprocess(i):

    ck=i['ck_kernel']
    rt=i['run_time']
    deps=i['deps']

    ck.out('***********************************')
    ck.out('Resolved deps via CK:')
    ck.out('')
    ck.out(json.dumps(deps, indent=2))
    ck.out('***********************************')

    env=i['env']
    nenv={} # new environment to be added to the run script

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']
    remote=tosd.get('remote','')

    if remote=='yes':
       es=tosd['env_set']
    else:
       es=hosd['env_set'] # set or export

    ck_var1=int(env.get('CK_VAR1','0'))
    ck_var2=int(env.get('CK_VAR2','0'))

    ck_var3=ck_var1+ck_var2

    nenv['CK_VAR3']=ck_var3

    b=''

    return {'return':0, 'bat':b, 'new_env':nenv}

# Do not add anything here!
