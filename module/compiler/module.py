#
# Collective Knowledge (compiler choices)
#
# See CK LICENSE.txt for licensing details
# See CK Copyright.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://cTuning.org/lab/people/gfursin
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# extract choices to universal pipeline tuning

def extract_to_pipeline(i):
    """
    Input:  {
              (data_uoa) - compiler description
              (file_in)  - JSON pipeline template
              (file_out) - output prepared pipeline to this file
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              pipeline     - prepared pipeline
            }

    """

    fo=i.get('file_out','')
    fi=i.get('file_in','')
    duoa=i.get('data_uoa','')

    # Prepare pipeline template
    ck.out('Preparing pipeline template ...')

    if fi=='':
       fi=os.path.join(work['path'],cfg['pipeline_template'])

    r=ck.load_json_file({'json_file':fi})
    if r['return']>0: return r
    pipeline=r['dict']

    # Load or select compiler description
    ck.out('')
    ck.out('Selecting compiler and description ...')
    if duoa=='':
       rx=ck.access({'action':'search',
                     'module_uoa':work['self_module_uid']})
       if rx['return']>0: return rx
       lst=rx['lst']

       if len(lst)==0:
          duoa=''
       elif len(lst)==1:
          duid=lst[0]['data_uid']
          duoa=lst[0]['data_uoa']
       else:
          # SELECTOR *************************************
          ck.out('')
          ck.out('Multiple choices available:')
          ck.out('')
          r=ck.select_uoa({'choices':lst})
          if r['return']>0: return r
          duoa=r['choice']

    if duoa=='':
       return {'return':1, 'error':'no compiler description selected'}

    # Load compiler desc
    rx=ck.access({'action':'load',
                  'module_uoa':work['self_module_uid'],
                  'data_uoa':duoa})
    if rx['return']>0: return rx
    d=rx['dict']
    dsc=rx.get('desc',{})
    
    dx=dsc.get('all_compiler_flags_desc',{})
   
    # Update pipeline
    ck.out('')
    ck.out('Updating pipeline choices with compiler flags ...')

    if 'pipeline' not in pipeline: pipeline['pipeline']={}
    px=pipeline['pipeline']

    px['choices_desc']={}
    for q in dx:
        qq=dx[q]
        q1=q
        if q1.startswith('##'): q1=q1[1:]
        q1='##compiler_flags'+q1
        px['choices_desc'][q1]=qq

    # Saving file
    if fo!='':
       ck.out('')
       ck.out('Writing pipeline ...')

       rx=ck.save_json_to_file({'json_file':fo, 'dict':pipeline})
       if rx['return']>0: return rx

    return {'return':0, 'pipeline':pipeline}

##############################################################################
# extract optimization flags and parameters from a compiler for autotuning (currently GCC)

def extract_opts(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (target_os)            - OS module to check (if omitted, analyze host)
              (device_id)            - device id if remote (such as adb)

              (compiler_id)          - currently support only "gcc" (default)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import sys

    o=i.get('out','')

    comp_id=i.get('compiler_id','').lower()
    if comp_id=='': comp_id='gcc'

    # Check OS
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')

    # Get some info about platforms
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid}
    r=ck.access(ii)
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    tdid=r['device_id']

    sext=hosd.get('script_ext','')
    scall=hosd.get('env_call','')
    sbp=hosd.get('bin_prefix','')

    tags='compiler'
    if comp_id=='gcc': tags+=',gcc'

    # Get compiler env
    ii={'action':'set',
        'module_uoa':cfg['module_deps']['env'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'tags':tags,
        'out':o}
    r=ck.access(ii)
    if r['return']>0: return r

    env_uoa=r['env_uoa']
    bat=r['bat']

    # Detect version
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['soft'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'tags':tags,
        'env':bat}
    r=ck.access(ii)
    if r['return']>0: return r

    vstr=r['version_str']
    if o=='con':
       ck.out('Detected GCC version: '+vstr)

    # Prepare batch file
    rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'yes'})
    if rx['return']>0: return rx
    fbat=rx['file_name']

    # Prepare 2 tmp files
    rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':'.tmp', 'remove_dir':'yes'})
    if rx['return']>0: return rx
    fout1=rx['file_name']

    rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':'.tmp', 'remove_dir':'yes'})
    if rx['return']>0: return rx
    fout2=rx['file_name']

    # Prepare GCC help
    bat+='\n'
    bat+=scall+' gcc --help=optimizer > '+fout1+'\n'
    bat+=scall+' gcc --help=params > '+fout2+'\n'

    # Save file
    rx=ck.save_text_file({'text_file':fbat, 'string':bat})
    if rx['return']>0: return rx

    # Execute 
    y=scall+' '+sbp+fbat

    if o=='con':
       ck.out('')
       ck.out('Executing prepared batch file '+fbat+' ...')

    sys.stdout.flush()
    rx=os.system(y)

    os.remove(fbat)
    
    # Load files
    rx=ck.load_text_file({'text_file':fout1,
                          'split_to_list':'yes', 
                          'encoding':sys.stdin.encoding,
                          'delete_after_read':'yes'})
    if rx['return']>0: return rx
    lopts=rx['lst']

    rx=ck.load_text_file({'text_file':fout2,
                          'split_to_list':'yes', 
                          'encoding':sys.stdin.encoding,
                          'delete_after_read':'yes'})
    if rx['return']>0: return rx
    lparams=rx['lst']

    # Parsing opts
    dd={"##base_opt": {
            "choice": [
              "-O3", 
              "-Ofast", 
              "-O0", 
              "-O1", 
              "-O2", 
              "-Os"
            ], 
            "default": "", 
            "desc": "base compiler flag", 
            "sort": 10000, 
            "tags": [
              "base", 
              "basic", 
              "optimization"
            ], 
            "type": "text"
          }
       }

    iopt=0
    iparam=0

    opt=''
    opt1=''
    desc=''
    desc1=''

    add=False
    finish=False

    for q in range(1, len(lopts)):
        qq=lopts[q]
        if len(qq)>2:
           if qq[2]=='-':
              qq=qq.strip()
              j=qq.find(' ')
              desc1=''
              if j>=0:
                 desc1=qq[j:].strip()
              else:
                 j=len(qq)
              opt1=qq[1:j]

              if not opt1.startswith('O'):
                 if opt=='': 
                    opt=opt1
                    desc=desc1
                 else:
                    add=True

           else:
              qq=qq.strip()
              if len(qq)>0:
                 desc+=' '+qq
        else:
           add=True
           finish=True

        if add and opt!='':
           iopt+=1

           ck.out('Adding '+str(iopt)+' "'+opt+'" - '+desc)

           dd['##'+opt]={
             "can_omit": "yes", 
             "choice": [
               "-f"+opt, 
               "-fno-"+opt
             ], 
             "default": "", 
             "desc": "compiler flag: -f"+opt+"("+desc+")", 
             "sort": iopt*100, 
             "tags": [
               "basic", 
              "optimization"
             ], 
             "type":"text"
           }

           opt=opt1 	
           desc=desc1

           add=False

        if finish: 
           break

    return {'return':0}
