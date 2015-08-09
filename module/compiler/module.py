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
# Note: GCC sources are needed - this script searches for GCC opts in all sub-directories
#       in a current directory. Therefore, just untar all GCC sources in current directory.
#
# (partially based on scripts from Abdul Wahid Memon and Yuriy Kashnikov)

def extract_opts(i):
    """
    Input:  {
              (record)               - if 'yes, record to repo
              (repo_uoa)             - repo UOA to record compiler description
              (data_uoa)             - data UOA to record compiler description (if empty, autogenerate)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import sys
    import datetime

    o=i.get('out','')

    p=os.getcwd()

    f1a=cfg['gcc_src_opt_file1']
    f1b=cfg['gcc_src_opt_file2']
    f2=cfg['gcc_src_params']

    results={}

    # Checking if GCC 
    try:
       dirList=os.listdir(p)
    except Exception as e:
        None
    else:
        for fn in dirList:
            pp=os.path.join(p, fn)
            if os.path.isdir(pp) and fn.startswith('gcc-'):
               found=False

               p1a=os.path.join(pp,f1a)
               p1b=os.path.join(pp,f1b)
               p2=os.path.join(pp,f2)

               if os.path.isfile(p1a) or os.path.isfile(p1b) or os.path.isfile(p2):
                  # Found GCC source directory with needed files
                  ck.out('*************************************')
                  ck.out('Processing GCC directory: '+fn)

                  ck.out('')

                  ver=fn[4:]
                  lver=ver.split('.')

                  dd={}

                  iopt=0
                  iparam=0

                  p1=''
                  if os.path.isfile(p1a):
                     p1=p1a
                  elif os.path.isfile(p1b):
                     p1=p1b

                  if p1!='':
                     # Load opt file
                     rx=ck.load_text_file({'text_file':p1,
                                           'split_to_list':'yes', 
                                           'encoding':sys.stdin.encoding})
                     if rx['return']>0: return rx
                     lopts=rx['lst']

                     found=False
                     for q in range(0, len(lopts)):
                         qq=lopts[q].strip()

                         if not found:
                            if qq=='@item Optimization Options':
                               ck.out('Found optimization flags')
                               found=True
                         else:
                            if qq.startswith('@end ') or qq=='':
                               break

                            if qq.startswith('@gccoptlist{'):
                               qq=qq[11:]
                            elif qq.startswith('@'):
                               continue                               

                            if qq.endswith('@gol'):
                               qq=qq[:-5]

                            jj=qq.split(' ')

                            # Check if base flag
                            if len(jj)>0 and jj[0].startswith('-O'):
                               choice=[]
                               if '-O3' in jj: choice.append('-O3')
                               for j in jj:
                                   if j!='' and j!='-O3' and j!='-O':
                                      choice.append(j)

                               dd["##base_opt"]={
                                       "choice": choice,
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

                            else:
                               for j in jj:
                                   if j!='' and not j.startswith('--param') and not j.startswith('@') and j.startswith('-f'):
                                      if '@' in j:
                                         iparam+=1

                                         ij=j.find('@')
                                         opt=j[:ij]

                                         ck.out('Adding param '+str(iparam)+' '+opt)

                                         dd['##param_'+opt]={
                                           "can_omit": "yes", 
                                           "default": "", 
                                           "desc": "compiler flag: "+j, 
                                           "sort": iparam*100+30000, 
                                           "explore_prefix": j, 
                                           "explore_start": 0, 
                                           "explore_step": 1, 
                                           "explore_stop": 0, 
                                           "tags": [
                                             "basic", 
                                            "optimization"
                                           ], 
                                           "type":"integer"
                                         }

                                      else:
                                         iopt+=1

                                         opt=j[2:]

                                         ck.out('Adding opt '+str(iopt)+' '+j)

                                         dd['##'+opt]={
                                           "can_omit": "yes", 
                                           "choice": [
                                             "-f"+opt, 
                                             "-fno-"+opt
                                           ], 
                                           "default": "", 
                                           "desc": "compiler flag: "+j, 
                                           "sort": iopt*100, 
                                           "tags": [
                                             "basic", 
                                            "optimization"
                                           ], 
                                           "type":"text"
                                         }

                  # Checking params
                  if os.path.isfile(p2):
                     # Load opt file
                     rx=ck.load_text_file({'text_file':p2,
                                           'split_to_list':'yes', 
                                           'encoding':sys.stdin.encoding})
                     if rx['return']>0: return rx
                     lparams=rx['lst']

                     # Parsing params
                     opt=''
                     opt1=''
                     desc=''
                     desc1=''

                     add=False
                     finish=False

                     for q in range(0, len(lparams)):
                         qq=lparams[q].strip()
                         if qq.startswith('DEFPARAM'):
                            iparam+=1

                            q+=1
                            opt=lparams[q].strip()[1:-2]

                            q+=1
                            desc=lparams[q].strip()[1:-2]
                            line='x'
                            while True:
                               q+=1
                               line=lparams[q].strip()
                               if line[-1]==')': break
                               desc+=line[1:-2]

                            e1=0
                            e2=0

                            exp=line[:-1].split(',')

                            skip=False
                            for j in range(0, len(exp)):
                                jj=exp[j].strip()
                                if jj.find('*')>0 or jj.find('_')>0:
                                   skip=True
                                else:
                                   jj=int(exp[j].strip())
                                   exp[j]=jj

                            if not skip:
                               if len(exp)>1 and exp[2]>exp[1]:
                                  e1=exp[1]
                                  e2=exp[2]
                               else:
                                  e1=0
                                  e2=exp[0]*2

                               ck.out('Adding param '+str(iparam)+' "'+opt+'" - '+desc)

                               dd['##param_'+opt]={
                                 "can_omit": "yes", 
                                 "default": "", 
                                 "desc": "compiler flag: --param "+opt+"= ("+desc+")", 
                                 "sort": iparam*100+30000, 
                                 "explore_prefix": "--param "+opt+"=", 
                                 "explore_start": e1, 
                                 "explore_step": 1, 
                                 "explore_stop": e2, 
                                 "tags": [
                                   "basic", 
                                  "optimization"
                                 ], 
                                 "type":"integer"
                               }

                  # Prepare CK entry
                  if i.get('record','')=='yes':
                     duoa=i.get('data_uoa','')
                     if duoa=='':
                        duoa=fn+'-auto'

                     if o=='con':
                        ck.out('')
                        ck.out('Recording to '+duoa+' ...')

                     ii={'action':'add',
                         'module_uoa':work['self_module_uid'],
                         'repo_uoa':i.get('repo_uoa',''),
                         'data_uoa':duoa,
                         'desc':{'all_compiler_flags_desc':dd},
                         'dict':{
                           "tags": [
                             "compiler", 
                             "gcc", 
                             "v"+lver[0], 
                             "v"+lver[0]+"."+lver[1],
                             "auto"
                           ]
                         }
                        }
                     r=ck.access(ii)
                     if r['return']>0: return r

                  p9=os.path.join(pp, 'ChangeLog')
                  year=''
                  if os.path.isfile(p9):
                     t = os.path.getmtime(p9)
                     t1=str(datetime.datetime.fromtimestamp(t))
                     year=t1[:4]

                  results[fn]={'boolean_opts':iopt, 'parametric_opts':iparam, 'year':year}

                  # Final info
                  if o=='con':
                     ck.out('')
                     ck.out('Compiler:                     '+str(fn))
                     ck.out('  Year:                       '+year)
                     ck.out('  Number of boolean opts:     '+str(iopt))
                     ck.out('  Number of parameteric opts: '+str(iparam))

    # Summary
    if len(results)>0:
       ck.out('*********************************************************')
       for q in sorted(list(results.keys())):
           qq=results[q]

           x=qq['year']+', '

           ib=str(qq['boolean_opts'])
           x+=' '*(6-len(ib))+ib+', '

           ip=str(qq['parametric_opts'])
           x+=' '*(6-len(ip))+ip+', '

           x+=q+' '*(10-len(q))

           ck.out(x)

    return {'return':0}

##############################################################################
# extract optimization flags and parameters from a compiler for autotuning (currently GCC)

def extract_opts_new(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (target_os)            - OS module to check (if omitted, analyze host)
              (device_id)            - device id if remote (such as adb)

              (compiler_id)          - currently support only "gcc" (default)

              (repo_uoa)             - repo UOA to record compiler description
              (data_uoa)             - data UOA to record compiler description (if empty, autogenerate)
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

    # Prepare GCC help
    bat+='\n'
    bat+='gcc --help=optimizer > '+fout1+'\n'

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
    
    # Load opt file
    rx=ck.load_text_file({'text_file':fout1,
                          'split_to_list':'yes', 
                          'encoding':sys.stdin.encoding,
                          'delete_after_read':'yes'})
    if rx['return']>0: return rx
    lopts=rx['lst']

    # Check if want params
    ck.out('')
    r=ck.inp({'text':'Enter full path to params.def file if you have GCC sources (or Enter to skip it): '})
    if r['return']>0: return r

    fpar=r['string'].strip()
    
    lparams=[]
    if fpar!='':
       rx=ck.load_text_file({'text_file':fpar,
                             'split_to_list':'yes', 
                             'encoding':sys.stdin.encoding})
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

           ck.out('Adding opt '+str(iopt)+' "'+opt+'" - '+desc)

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

    # Parsing params
    opt=''
    opt1=''
    desc=''
    desc1=''

    add=False
    finish=False

    for q in range(0, len(lparams)):
        qq=lparams[q].strip()
        if qq.startswith('DEFPARAM'):
           iparam+=1

           q+=1
           opt=lparams[q].strip()[1:-2]

           q+=1
           desc=lparams[q].strip()[1:-2]
           line='x'
           while True:
              q+=1
              line=lparams[q].strip()
              if line[-1]==')': break
              desc+=line[1:-2]

           e1=0
           e2=0

           exp=line[:-1].split(',')

           skip=False
           for j in range(0, len(exp)):
               jj=exp[j].strip()
               if jj.find('*')>0 or jj.find('_')>0:
                  skip=True
               else:
                  jj=int(exp[j].strip())
                  exp[j]=jj

           if not skip:
              if exp[2]>exp[1]:
                 e1=exp[1]
                 e2=exp[2]
              else:
                 e1=0
                 e2=exp[0]*2

              ck.out('Adding param '+str(iparam)+' "'+opt+'" - '+desc)

              dd['##param_'+opt]={
                "can_omit": "yes", 
                "default": "", 
                "desc": "compiler flag: --param "+opt+"= ("+desc+")", 
                "sort": iparam*100+30000, 
                "explore_prefix": "--param "+opt+"=", 
                "explore_start": e1, 
                "explore_step": 1, 
                "explore_stop": e2, 
                "tags": [
                  "basic", 
                 "optimization"
                ], 
                "type":"integer"
              }

    # Prepare CK entry
    duoa=i.get('data_uoa','')
    if duoa=='':
       v=vstr.split('.')
       duoa='gcc-'+v[0]+v[1]+'x'

    if o=='con':
       ck.out('')
       ck.out('Recording to '+duoa+' ...')

    ii={'action':'add',
        'module_uoa':work['self_module_uid'],
        'repo_uoa':i.get('repo_uoa',''),
        'data_uoa':duoa,
        'desc':{'all_compiler_flags_desc':dd},
        'dict':{
          "tags": [
          "compiler", 
          "gcc", 
          "v"+v[0], 
          "v"+v[0]+"."+v[1]
          ]
        }
       }
    r=ck.access(ii)
    if r['return']>0: return r

    # Final info
    if o=='con':
       ck.out('')
       ck.out('Compiler version:           '+vstr)
       ck.out('Number of boolean opts:     '+str(iopt))
       ck.out('Number of parameteric opts: '+str(iparam))

    return {'return':0}
