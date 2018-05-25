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

    # example of reading and concatenating stdout and stderr
    rf1=rt['run_cmd_out1']
    rf2=rt['run_cmd_out2']

    lst=[]

    if os.path.isfile(rf1):
       r=ck.load_text_file({'text_file':rf1,'split_to_list':'yes'})
       if r['return']>0: return r
       lst+=r['lst']
    if os.path.isfile(rf2):
       r=ck.load_text_file({'text_file':rf2,'split_to_list':'yes'})
       if r['return']>0: return r
       lst+=r['lst']

    # Load output from xOpenME
    r=ck.load_json_file({'json_file':'tmp-ck-timer.json'})
    if r['return']>0: return r

    d=r['dict']

    rts=d['run_time_state']

    ck_var1=int(rts['ck_var1'])
    ck_var2=int(rts['ck_var2'])
    ck_var3=int(rts['ck_var3'])

    rts['ck_var4']=ck_var1+ck_var2+ck_var3

    d['post_processed']='yes'

    # Save to file.
    r=ck.save_json_to_file({'json_file':'tmp-ck-timer.json', 'dict':d})
    if r['return']>0: return r

    return {'return':0}

# Do not add anything here!
