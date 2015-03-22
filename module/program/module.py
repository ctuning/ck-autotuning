#
# Collective Knowledge (program)
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
sep='***************************************************************************************'

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
# compile program

def process(i):
    """
    Input:  {
              sub_action   - clean, compile, run

              (repo_uoa)   - program repo UOA
              (module_uoa) - program module UOA
              data_uoa     - program data UOA

              (process_in_tmp)       - (default 'yes') - if 'yes', clean, compile and run in the tmp directory 
              (tmp_dir)              - (default 'tmp') - if !='', use this tmp directory to clean, compile and run
              (generate_rnd_tmp_dir) - if 'yes', generate random tmp directory            
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              Output of the last compile from function 'process_in_dir'

              tmp_dir      - directory where clean, compile, run
            }

    """

    import os
    import copy

    ic=copy.deepcopy(i)

    # Check if global writing is allowed
    r=ck.check_writing({})
    if r['return']>0: return r

    o=i.get('out','')

    a=i.get('repo_uoa','')
    m=i.get('module_uoa','')
    duoa=i.get('data_uoa','')

    lst=[]

    if duoa=='':
       # First, try to detect CID in current directory
       r=ck.cid({})
       if r['return']==0:
          a=r.get('repo_uoa','')
          m=r.get('module_uoa','')
          duoa=r.get('data_uoa','')

       if duoa=='':
          # Attempt to load configuration from the current directory
          p=os.getcwd()

          pc=os.path.join(p, ck.cfg['subdir_ck_ext'], ck.cfg['file_meta'])
       
          if os.path.isfile(pc):
             r=ck.load_json_file({'json_file':pc})
             if r['return']==0:
                d=r['dict']

                ii=copy.deepcopy(ic)
                ii['path']=p
                ii['meta']=d
                return process_in_dir(ii)

          return {'return':1, 'error':'data UOA is not defined'}

    # Check wildcards
    if a.find('*')>=0 or a.find('?')>=0 or m.find('*')>=0 or m.find('?')>=0 or duoa.find('*')>=0 or duoa.find('?')>=0: 
       r=ck.list_data({'repo_uoa':a, 'module_uoa':m, 'data_uoa':duoa})
       if r['return']>0: return r

       lst=r['lst']
    else:
       # Find path to data
       r=ck.find_path_to_data({'repo_uoa':a, 'module_uoa':m, 'data_uoa':duoa})
       if r['return']>0: return r
       p=r['path']
       ruoa=r.get('repo_uoa','')
       ruid=r.get('repo_uid','')
       muoa=r.get('module_uoa','')
       muid=r.get('module_uid','')
       duid=r.get('data_uid','')
       duoa=r.get('data_alias','')
       if duoa=='': duoa=duid

       lst.append({'path':p, 'repo_uoa':ruoa, 'repo_uid':ruid, 
                             'module_uoa':muoa, 'module_uid':muid, 
                             'data_uoa':duoa, 'data_uid': duid})

    r={'return':0}
    for ll in lst:
        p=ll['path']

        ruid=ll['repo_uid']
        muid=ll['module_uid']
        duid=ll['data_uid']

        r=ck.access({'action':'load',
                     'repo_uoa':ruid,
                     'module_uoa':muid,
                     'data_uoa':duid})
        if r['return']>0: return r
 
        d=r['dict']

        if o=='con':
           ck.out('')

        ii=copy.deepcopy(ic)
        ii['path']=p
        ii['meta']=d
        ii['repo_uoa']=ruid
        ii['module_uoa']=muid
        ii['data_uoa']=duid
        r=process_in_dir(ii)
        if r['return']>0: return r

    return r      

##############################################################################
# compile program  (called from universal function here)

def process_in_dir(i):
    """
    Input:  {
              The same as 'compile'

              sub_action         - clean, compile, run

              path               - path
              meta               - program description

              (flags)            - compile flags
              (lflags)           - link flags

              (compile_type)     - static or dynamic (dynamic by default)

              (repeat)           - repeat kernel via environment CT_REPEAT_MAIN if supported

              (clean)            - if 'yes', clean tmp directory before using
              (skip_clean_after) - if 'yes', do not remove run batch

              (repo_uoa)         - program repo UOA
              (module_uoa)       - program module UOA
              (data_uoa)         - program data UOA

              (misc)             - misc  dict
              (characteristics)  - characteristics/features/properties
              (env)              - preset environment

              (deps)             - already resolved deps (useful for auto-tuning)
            }

    Output: {
              return          - return code =  0, if successful
                                            >  0, if error
              (error)         - error text if return > 0

              misc            - updated misc dict
              characteristics - updated characteristics
              env             - updated environment
              deps            - resolved deps, if any
            }

    """
    import os
    import time
    import sys
    import shutil

    start_time=time.time()

    sys.stdout.flush()

    o=i.get('out','')

    misc=i.get('misc',{})
    ccc=i.get('characteristics',{})
    env=i.get('env',{})
    deps=i.get('deps',{})

    flags=i.get('flags','')
    lflags=i.get('lflags','')
    repeat=i.get('repeat','')
    ctype=i.get('compile_type','')
    if ctype=='': ctype='dynamic'

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'host_os':hos,
                 'target_os':tos,
                 'target_device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    tbits=tosd.get('bits','')

    # update misc
    misc['host_os_uoa']=hosx
    misc['target_os_uoa']=tosx
    misc['target_device_id']=tdid

    # Get host platform type (linux or win)
    rx=ck.get_os_ck({})
    if rx['return']>0: return rx
    hplat=rx['platform']

    rem=hosd.get('rem','')
    eset=hosd.get('env_set','')
    svarb=hosd.get('env_var_start','')
    svare=hosd.get('env_var_stop','')
    scall=hosd.get('env_call','')
    sdirs=hosd.get('dir_sep','')
    sext=hosd.get('script_ext','')
    sexe=hosd.get('set_executable','')
    se=tosd.get('file_extensions',{}).get('exe','')
    sbp=hosd.get('bin_prefix','')
    sqie=hosd.get('quit_if_error','')
    evs=hosd.get('env_var_separator','')
    eifs=hosd.get('env_quotes_if_space','')
    eifsc=hosd.get('env_quotes_if_space_in_call','')
    wb=tosd.get('windows_base','')

    ########################################################################
    # Prepare some params
    misc=i.get('misc',{})
    misc.update({'host_os_uoa':hos,
                 'target_os_uoa':tos,
                 'target_os_bits':tbits})

    # Get host platform
    rx=ck.get_os_ck({})
    if rx['return']>0: return rx
    ios=rx['platform']

    p=i['path']
    meta=i['meta']

    ruoa=i.get('repo_uoa', '')
    muoa=i.get('module_uoa', '')
    duoa=i.get('data_uoa', '')

    target_exe=meta.get('target_file','')
    if target_exe=='':
       target_exe=cfg.get('target_file','')
    target_exe+=se

    # If muoa=='' assume program
    if muoa=='':
       muoa=work['self_module_uid']

    if duoa=='':
       x=meta.get('backup_data_uid','')
       if x!='':
          duoa=meta['backup_data_uid']

    # Check if compile in tmp dir
    cdir=p
    os.chdir(cdir)

    sa=i['sub_action']

    ################################### Run ######################################
    if sa=='clean':
       # Get host platform type (linux or win)
       cmd=cfg.get('clean_cmds',{}).get(hplat)

       if o=='con':
          ck.out(cmd)
          ck.out('')

       rx=os.system(cmd)

       # Removing tmp directories
       curdir=os.getcwd()
       for q in os.listdir(curdir):
           if not os.path.isfile(q) and q.startswith('tmp'):
              shutil.rmtree(q, ignore_errors=True)

       return {'return':0}

    # Check tmp dir ...
    x=i.get('process_in_tmp','').lower()
    if x=='': x='yes'

    if x!='yes':
       x=meta.get('process_in_tmp','').lower()

    if x=='yes':
       td=i.get('tmp_dir','')
       if td=='': td='tmp'

       if i.get('clean','')=='yes':
          if td!='' and os.path.isdir(td):
             shutil.rmtree(td, ignore_errors=True)

       if i.get('generate_rnd_tmp_dir','')=='yes':
          # Generate tmp dir
          import tempfile
          fd, fn=tempfile.mkstemp(suffix='', prefix='tmp-ck-')
          os.close(fd)
          os.remove(fn)

          cdir=os.path.join(p, fn)
       else:
          cdir=os.path.join(p, td)

    misc['tmp_dir']=td

    if cdir!='' and not os.path.isdir(cdir):
       os.mkdir(cdir)

    sb='' # Batch

    os.chdir(cdir)
    rcdir=os.getcwd()

    # If run and dynamic, check deps prepared by compiler
    fdeps=cfg.get('deps_file','')
    if len(deps)==0 and ctype=='dynamic' and sa=='run':
       if os.path.isfile(fdeps):
          ck.out('')
          ck.out('Reloading depedencies from compilation '+fdeps+' ...')

          rx=ck.load_json_file({'json_file':fdeps})
          if rx['return']>0: return rx
          deps=rx['dict']

    # If compile type is dynamic, reuse deps even for run (to find specific DLLs)
    if (ctype=='dynamic' or sa=='compile'):
       # Resolve deps (if not ignored, such as when installing local version with all dependencies set)
       if len(deps)==0: 
          deps=meta.get('compile_deps',{})

       if len(deps)>0:
          if o=='con':
             ck.out(sep)

          ii={'action':'resolve',
              'module_uoa':cfg['module_deps']['env'],
              'host_os':hos,
              'target_os':tos,
              'target_device_id':tdid,
              'deps':deps,
              'add_customize':'yes'}
          if o=='con': ii['out']='con'

          rx=ck.access(ii)
          if rx['return']>0: return rx
          sb+=rx['bat']
          deps=rx['deps'] # Update deps (add UOA)

       if sa=='compile':
          rx=ck.save_json_to_file({'json_file':fdeps, 'dict':deps})
          if rx['return']>0: return rx

    # If compiler, load env
    comp=deps.get('compiler',{})
    comp_uoa=comp.get('uoa','')
    dcomp={}
    
    if comp_uoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['env'],
                     'data_uoa':comp_uoa})
       if rx['return']>0: return rx
       dcomp=rx['dict']

    # Check sub_actions
    ################################### Compile ######################################
    if sa=='compile':
       # Add env
       for k in sorted(env):
           v=env[k]

           if eifs!='' and wb!='yes':
              if v.find(' ')>=0 and not v.startswith(eifs):
                 v=eifs+v+eifs

           sb+=eset+' '+k+'='+v+'\n'
       sb+='\n'

       # Check linking libs + include paths for deps
       sll=''
       sin=''
       for k in deps:
           kv=deps[k].get('cus',{})

           pl1=kv.get('path_lib','')
           pl2=kv.get('static_lib','')
           if pl2!='':
              if sll!='': sll+=' '
              sll+=eifsc
              if pl1!='': 
                 sll+=pl1+sdirs
              sll+=pl2+eifsc

           pl3=kv.get('path_include','')
           if pl3!='':
              if sin!='': sin+=' '
              sin+=svarb+'CK_FLAG_PREFIX_INCLUDE'+svare+eifsc+pl3+eifsc

       # Obtaining compile CMD (first from program entry, then default from this module)
       ccmds=meta.get('compile_cmds',{})
       ccmd=ccmds.get(hplat,{})
       if len(ccmd)==0:
          ccmd=ccmds.get('default',{})
       if len(ccmd)==0:
          ccmds=cfg.get('compile_cmds',{})
          ccmd=ccmds.get(hplat,{})
          if len(ccmd)==0:
             ccmd=ccmds.get('default',{})
       
       sccmd=ccmd.get('cmd','')
       if sccmd=='':
          return {'return':1, 'error':'compile CMD is not found'}

       # Source files
       sfs=meta.get('source_files',[])

       compiler_env=meta.get('compiler_env','')
       if compiler_env=='': compiler_env='CK_CC'

       sfprefix='..'+sdirs
       
       scfb=svarb+'CK_FLAGS_CREATE_OBJ'+svare
       scfb+=' '+svarb+'CK_COMPILER_FLAGS_OBLIGATORY'+svare
       if ctype=='dynamic':
          scfb+=' '+svarb+'CK_FLAGS_DYNAMIC_BIN'+svare
       elif ctype=='static':
          scfb+=' '+svarb+'CK_FLAGS_STATIC_BIN'+svare
       scfb+=' '+svarb+'CK_FLAG_PREFIX_INCLUDE'+svare+sfprefix

       scfa=''

       # Check build -D flags
       sbcv=''
       bcv=meta.get('build_compiler_vars',{})
       for k in bcv:
           kv=bcv[k]
           if sbcv!='': sbcv+=' '
           sbcv+=svarb+'CK_FLAG_PREFIX_VAR'+svare+k
           if kv!='': sbcv+='='+kv

       # Prepare compilation
       sb+='\n'

       sobje=dcomp.get('env',{}).get('CK_OBJ_EXT','')
       sofs=''
       xsofs=[]

       for sf in sfs:
           xcfb=scfb
           xcfa=scfa

           sf0,sf1=os.path.splitext(sf)

           sfobj=sf0+sobje
           if sofs!='': sofs+=' '
           sofs+=sfobj
           xsofs.append(sfobj)

           if sbcv!='': xcfb+=' '+sbcv

           if sin!='': xcfb+=' '+sin

           xcfb+=' '+flags

           xcfa+=' '+svarb+'CK_FLAGS_OUTPUT'+svare+sfobj

           cc=sccmd
           cc=cc.replace('$#source_file#$', sfprefix+sf)

           cc=cc.replace('$#compiler#$', svarb+compiler_env+svare)

           cc=cc.replace('$#flags_before#$', xcfb)
           cc=cc.replace('$#flags_after#$', xcfa)

           sb+='echo '+eifs+cc+eifs+'\n'
           sb+=cc+'\n'
           sb+=sqie+'\n'

           sb+='\n'

       # Obtaining link CMD (first from program entry, then default from this module)
       if sofs!='':
          linker_env=meta.get('linker_env','')
          if linker_env=='': linker_env=compiler_env

          lcmds=meta.get('link_cmds',{})
          lcmd=lcmds.get(hplat,{})
          if len(lcmd)==0:
             lcmd=lcmds.get('default',{})
          if len(lcmd)==0:
             lcmds=cfg.get('link_cmds',{})
             lcmd=lcmds.get(hplat,{})
             if len(lcmd)==0:
                lcmd=lcmds.get('default',{})
          
          slcmd=lcmd.get('cmd','')
          if slcmd!='':
             slfb=svarb+'CK_COMPILER_FLAGS_OBLIGATORY'+svare
             slfb+=' '+lflags
             if ctype=='dynamic':
                slfb+=' '+svarb+'CK_FLAGS_DYNAMIC_BIN'+svare
             elif ctype=='static':
                slfb+=' '+svarb+'CK_FLAGS_STATIC_BIN'+svare

             slfa=' '+svarb+'CK_FLAGS_OUTPUT'+svare+target_exe
             slfa+=' '+svarb+'CK_LD_FLAGS_MISC'+svare
             slfa+=' '+svarb+'CK_LD_FLAGS_EXTRA'+svare

             if sll!='': slfa+=' '+sll

             cc=slcmd
             cc=cc.replace('$#linker#$', svarb+linker_env+svare)
             cc=cc.replace('$#obj_files#$', sofs)
             cc=cc.replace('$#flags_before#$', slfb)
             cc=cc.replace('$#flags_after#$', slfa)

             sb+='echo '+eifs+cc+eifs+'\n'
             sb+=cc+'\n'
             sb+=sqie+'\n'

       # Record to tmp batch and run
       rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'yes'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       rx=ck.save_text_file({'text_file':fn, 'string':sb})
       if rx['return']>0: return rx

       y=''
       if sexe!='':
          y+=sexe+' '+sbp+fn+evs
       y+=' '+scall+' '+sbp+fn

       sys.stdout.flush()
       start_time1=time.time()
       rx=os.system(y)
       ccc['compilation_time']=time.time()-start_time1

       if rx>0:
          misc['compilation_success']='no'
       else:
          misc['compilation_success']='yes'

          # Check some characteristics
          if os.path.isfile(target_exe):
             ccc['binary_size']=os.path.getsize(target_exe)

          # Check obj file sizes
          ofs=0
          if len(xsofs)>0:
             ccc['obj_sizes']={}
             for q in xsofs:
                 if os.path.isfile(q):
                    ofs1=os.path.getsize(q)
                    ccc['obj_sizes'][q]=ofs1
                    ofs+=ofs1
             ccc['obj_size']=ofs

       ccc['compilation_time_with_module']=time.time()-start_time

    ################################### Run ######################################
    elif sa=='run':
       start_time=time.time()

       # Update environment
       env1=meta.get('run_vars',{})
       for q in env1:
           if q not in env:
              env[q]=env1[q]

       # Update env if repeat
       if repeat!='':
          env['CT_REPEAT_MAIN']=repeat

       # Add env
       for k in sorted(env):
           v=env[k]

           if eifs!='' and wb!='yes':
              if v.find(' ')>=0 and not v.startswith(eifs):
                 v=eifs+v+eifs

           sb+=eset+' '+k+'='+v+'\n'
       sb+='\n'

       # Check cmd key
       run_cmds=meta.get('run_cmds',{})
       if len(run_cmds)==0:
          return {'return':1, 'error':'no CMD for run'}

       krun_cmds=sorted(list(run_cmds.keys()))

       kcmd=i.get('cmd_key','')
       if kcmd=='':
          if 'default' in krun_cmds: kcmd='default'
          else: 
             kcmd=krun_cmds[0]








       else:
          if kcmd not in krun_cmds:
             return {'return':1, 'error':'CMD key not found in program description'}

       # Command line key is set
       vcmd=run_cmds[kcmd]
       misc['cmd_keys']=kcmd

       c=''

       rt=vcmd.get('run_time',{})

       c=rt.get('run_cmd_main','')
       if c=='':
          return {'return':1, 'error':'cmd is not defined'}

       # Replace bin file
       c=c.replace('$#BIN_FILE#$', sbp+target_exe)
       c=c.replace('$#os_dir_separator#$', os.sep)
       c=c.replace('$#src_path#$', p+sdirs)

       # Check if takes datasets from CK
       dtags=vcmd.get('dataset_tags',[])
       dduoa=i.get('dataset_uoa','')
       if dduoa!='' or len(dtags)>0:
          if dduoa=='':
             misc['dataset_tags']=dtags

             tags=''
             for q in dtags:
                 if tags!='': tags+=','
                 tags+=q

             dmuoa=cfg['module_deps']['dataset']
             dduoa=i.get('dataset_uoa','')
             if dduoa=='':
                rx=ck.access({'action':'search',
                              'module_uoa':dmuoa,
                              'tags':tags})
                if rx['return']>0: return rx
                lst=rx['lst']              
                              
                if len(lst)==0:
                   return {'return':1, 'error':'no related datasets found (tags='+tags+')'}  
                elif len(lst)==1:
                   dduoa=lst[0].get('data_uid','')
                else:
                   dduoa=lst[0].get('data_uid','')














          if dduoa=='':
             return {'return':1, 'error':'dataset is not specified'}  

          # Try to load dataset
          rx=ck.access({'action':'load',
                        'module_uoa':dmuoa,
                        'data_uoa':dduoa})
          if rx['return']>0: return rx
          dd=rx['dict']
          dp=rx['path']

          c=c.replace('$#dataset_path#$',dp)

          dfiles=dd.get('dataset_files',[])
          if len(dfiles)>0:
             for k in range(0, len(dfiles)):
                 df=dfiles[k]
                 kk='$#dataset_filename'
                 if k>0: kk+='_'+str(k)
                 kk+='#$'
                 c=c.replace(kk, df)

          rcm=dd.get('cm_properties',{}).get('run_time',{}).get('run_cmd_main',{})
          for k in rcm:
              kv=rcm[k]
              c=c.replace('$#'+k+'#$',kv)

          misc['dataset_uoa']=dduoa

       if o=='con': 
          ck.out(sep)
          ck.out(c)
          ck.out('')

       sb+=c+'\n'

       # Record to tmp batch and run
       rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'yes'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       rx=ck.save_text_file({'text_file':fn, 'string':sb})
       if rx['return']>0: return rx

       y=''
       if sexe!='':
          y+=sexe+' '+sbp+fn+evs
       y+=' '+scall+' '+sbp+fn

       sys.stdout.flush()
       start_time1=time.time()
       rx=os.system(y)
       ccc['execution_time']=time.time()-start_time1

       if rx>0 and vcmd.get('ignore_return_code','').lower()!='yes':
          misc['run_success']='no'
       else:
          misc['run_success']='yes'

       if i.get('skip_clean_after','')!='yes':
          if os.path.isfile(fn): os.remove(fn)

       ccc['execution_time_with_module']=time.time()-start_time

    return {'return':0, 'tmp_dir':rcdir, 'misc':misc, 'characteristics':ccc, 'deps':deps}

##############################################################################
# clean program work and tmp files

def clean(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    i['sub_action']='clean'
    return process(i)

##############################################################################
# compile program

def compile(i):
    """
    Input:  {
              (repo_uoa)   - program repo UOA
              (module_uoa) - program module UOA
              data_uoa     - program data UOA

              (process_in_tmp)
              (tmp_dir)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              Output of the last compile from function 'process_in_dir'
            }

    """

    i['sub_action']='compile'
    return process(i)

##############################################################################
# run program

def run(i):
    """
    Input:  {
               (cmd_key)     - cmd key
               (dataset_uoa) - dataset UOA
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    i['sub_action']='run'
    return process(i)

##############################################################################
# auto-tuning program

def autotune(i):
    """
    Input:  {
              (repo_uoa)   - program repo UOA
              (module_uoa) - program module UOA
              data_uoa     - program data UOA

              (process_in_tmp)
              (tmp_dir)

            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import os
    import random

    # Misc
    ic=copy.deepcopy(i)

    pp=os.getcwd()

    ni=i.get('number_of_iterations',0)
    try: ni=int(ni)
    except Exception as e: pass

    srm=i.get('stat_repetitions',0)
    try: srm=int(srm)
    except Exception as e: pass

    deps={}

    dflag=i.get('default_flag','')

    eruoa=i.get('experiment_repo_uoa','')
    euoa=i.get('experiment_uoa','')

    # Hack
    cduoa=i.get('compiler_desc_uoa','')
    if cduoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['compiler'],
                     'data_uoa':cduoa})
       if rx['return']>0: return rx
       cm=rx['dict']
       cc=cm.get('all_compiler_flags_desc',{})

    for m in range(0,ni+1):
        ck.out(sep)
        ck.out('Iteration: '+str(m))
        ck.out('')

        ii=copy.deepcopy(ic)
        ii['deps']=deps

        # Describing experiment
        dd={}

        dd['input']=ii
        dd['choices']={}
        dd['characteristics']={}
        dd['features']={}
        dd['misc']={}

        ##########################################################################################
        # Generate flags
        cflags=dflag
        if m!=0:
           cflags='-O3'
           for q in cc:
               if q!='##base_flag':
                  qx=cc[q]

                  stat=random.randrange(0, 1000)
                  if stat>900:
                     cqx=qx.get('choice',[])
                     lcqx=len(cqx)
                     if lcqx>0:
                        ln=random.randrange(0, lcqx)
                        cflags+=' '+cqx[ln]
                     else:
                        cflags+=''

        ck.out('Flags: '+cflags)

        ii['flags']=cflags

        dd['features']['compiler_flags']=cflags

        ##########################################################################################
        # Compile xyz
        os.chdir(pp)

        ck.out('')
        rx=compile(ii)
        if rx['return']>0: return rx 

        deps=rx['deps']
        cmisc=rx['misc']
        cch=rx['characteristics']

        xct=cch.get('compilation_time',-1)
        xos=cch.get('obj_size',-1)

        dd['characteristics']['compile']=cch
        dd['misc']['compile']=cmisc

        if xos>0:
           ##########################################################################################
           # Run
           ii['deps']=deps
           ii1=copy.deepcopy(ii)

           for sr in range(0, srm):
               ck.out('')
               ck.out('------------------- Statistical reptition: '+str(sr))
               ii=copy.deepcopy(ii1)

               os.chdir(pp)

               rx=run(ii)
               if rx['return']>0: return rx

               rmisc=rx['misc']
               rch=rx['characteristics']

               rsucc=rmisc.get('run_success','')
               dataset_uoa=rmisc.get('dataset_uoa','')
               xrt=rch.get('execution_time',-1)

               if rsucc=='yes' and xrt>0:
                  ck.out('')
                  ck.out('###### Compile time: '+str(xct)+', obj size: '+str(xos)+', run time: '+str(xrt))
                  ck.out('')

               dd['characteristics']['run']=rch
               dd['misc']['run']=rmisc

               ##########################################################################################
               # For now Process/record in expeirment, only if compile was successful
               # TBD: For compiler/architecture testing purposes, we may want to record failed cases in another repo

               
               ie={'action':'add',

                   'module_uoa':'experiment',

                   'ignore_update':'yes',

                   'experiment_repo_uoa': eruoa,
                   'experiment_uoa':euoa,

#                   'search_point_by_features':'yes',
#                   'process_multi_keys':['characteristics','features'],
                   'record_all_subpoints':'yes',

                   'search_point_by_features':'yes',
                   
                   'force_new_entry':'yes',

                   'sort_keys':'yes',
                   'out':'con',
                   'dict':dd}

               rx=ck.access(ie)
               if rx['return']>0: return rx

    return {'return':0}

##############################################################################
# crowdtuning program

def crowdtune(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    ck.out ('tbd: crowdtuning program')

    return {'return':0}
