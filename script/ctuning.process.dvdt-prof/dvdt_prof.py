#
# Copyright (c) 2017 cTuning foundation.
# See CK COPYRIGHT.txt for copyright details.
#
# SPDX-License-Identifier: BSD-3-Clause.
# See CK LICENSE.txt for licensing details.
#
# Convert raw dvdt prof output to the CK format.
#
# Developer(s):
#   - Grigori Fursin, cTuning foundation, 2017
#   - Anton Lokhmotov, dividiti, 2017
#

import json
import os
import re
import struct
import sys

def process(i):
    """
    Input:  {
              file_in  - stdout to parse
              file_out - file with raw dvdt prof data
              data     - dict with CK data to be updated
              env      - CK env to customize output if needed
                          CK_ADD_RAW_DVDT_PROF (if yes then add all raw data to CK pipeline)
              deps     - CK deps to get info about dvdt_prof
            }

    Output: {
              return        - return code =  0, if successful
                                          >  0, if error
              (error)       - error text if return > 0
            }

    """

    ck=i['ck_kernel']

    env=i['env']
    d=i['data']

    file_in=i['file_in']
    dvdt_prof_file=i['file_out']
    deps=i['deps']

    # Check if DVDT prof if actually used
    dvdt_prof_dep=deps.get('dvdt_prof',{})
    if dvdt_prof_dep.get('uoa','')!='':
        r=ck.save_json_to_file({'json_file':'tmp-dvdt-prof-deps.json', 'dict':dvdt_prof_dep, 'sort_keys':'yes'})
        if r['return']>0: return r

        # Load output.
        r=ck.load_text_file({
            'text_file':file_in,
            'split_to_list':'no'
        })
        if r['return']>0: return r

        # Locate profiler parser.
        dvdt_prof_dir=dvdt_prof_dep['dict']['env']['CK_ENV_TOOL_DVDT_PROF']
        dvdt_prof_src_python=os.path.join(dvdt_prof_dir,'src','python')

        sys.path.append(dvdt_prof_src_python)
        from prof_parser import prof_parse

        # Parse profiler output.
        dvdt_prof=prof_parse(r['string'])

        r=ck.save_json_to_file({'json_file':dvdt_prof_file, 'dict':dvdt_prof, 'sort_keys':'yes'})
        if r['return']>0: return r

        if env.get('CK_ADD_RAW_DVDT_PROF','').lower()=='yes':
           d['dvdt_prof']=dvdt_prof

        nqs=[ call for call in dvdt_prof if call['call'] in ['clEnqueueNDRangeKernel'] ]

#        d['execution_time_opencl_us']={ nq['name'] : (nq['profiling']['end']-nq['profiling']['start'])*1e-3 for nq in nqs }
#        d['execution_time_opencl_ms']={ nq['name'] : (nq['profiling']['end']-nq['profiling']['start'])*1e-6 for nq in nqs }
#        d['execution_time_opencl_s' ]={ nq['name'] : (nq['profiling']['end']-nq['profiling']['start'])*1e-9 for nq in nqs }

        d['execution_time_opencl_us']={}
        d['execution_time_opencl_ms']={}
        d['execution_time_opencl_s' ]={}

        d['execution_time_list_opencl']=[]

        seq=0
        for nq in nqs:
            kernel_name=nq['name']
            kernel_time=nq['profiling']['end']-nq['profiling']['start']

            d['execution_time_list_opencl'].append({'kernel_name':kernel_name, 
                                                    'kernel_time':kernel_time, 
                                                    'sequence':seq, 
                                                    'lws':nq.get('lws',[]),
                                                    'gws':nq.get('gws',[])})

            if kernel_name not in d['execution_time_opencl_us']:
               d['execution_time_opencl_us'][kernel_name]=0.0
               d['execution_time_opencl_ms'][kernel_name]=0.0
               d['execution_time_opencl_s' ][kernel_name]=0.0

            d['execution_time_opencl_us'][kernel_name]+=kernel_time*1e-3
            d['execution_time_opencl_ms'][kernel_name]+=kernel_time*1e-6
            d['execution_time_opencl_s' ][kernel_name]+=kernel_time*1e-9

            seq+=1

    return {'return':0}

def read_dvdt_prof(dvdt_prof_path='tmp-dvdt-prof.json'):
    # Return value.
    dvdt_prof={}

    with open(dvdt_prof_path, 'r') as dvdt_prof_file:
        dvdt_prof=json.load(dvdt_prof_file)

    return dvdt_prof
