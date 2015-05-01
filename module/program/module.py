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

              (host_os)        - host OS (detect, if omitted)
              (target_os)      - OS module to check (if omitted, analyze host)
              (device_id)      - device id if remote (such as adb)

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
              Comes from 'compile', 'run' and 'clean' functions

              sub_action             - clean, compile, run

              (host_os)        - host OS (detect, if omitted)
              (target_os)      - OS module to check (if omitted, analyze host)
              (device_id)      - device id if remote (such as adb)

              path                   - path
              meta                   - program description

              (generate_rnd_tmp_dir) - if 'yes', generate random tmp directory to compile and run program
                                       (useful during crowd-tuning)

              (compiler_vars)        - dict with set up compiler flags (-D xyz) -> 
                                       they will update the ones defined as default in program description ...

              (flags)                - compile flags
              (lflags)               - link flags

              (compile_type)         - static or dynamic (dynamic by default;
                                         however takes compiler default_compile_type into account)
                  or
              (static or dynamic)

              (repeat)               - repeat kernel via environment CT_REPEAT_MAIN if supported

              (clean)                - if 'yes', clean tmp directory before using
              (skip_clean_after)     - if 'yes', do not remove run batch

              (repo_uoa)             - program repo UOA
              (module_uoa)           - program module UOA
              (data_uoa)             - program data UOA

              (misc)                 - misc  dict
              (characteristics)      - characteristics/features/properties
              (env)                  - preset environment

              (deps)                 - already resolved deps (useful for auto-tuning)

              (extra_env)            - extra environment as string

              (console)              - if 'yes', output to console

              (skip_device_init)     - if 'yes', do not initialize device

              (skip_calibration)     - if 'yes', skip execution time calibration (make it around 4.0 sec)
              (calibration_time)     - calibration time in string, 4.0 sec. by default
              (calibration_max)      - max number of iterations for calibration, 10 by default

              (pull_only_timer_files) - if 'yes', pull only timer files, but not output files 
                                        (useful for remove devices during statistical repetition)

              (statistical_repetition) - int number of current (outside) statistical repetition
                                         to avoid pushing data to remote device if !=0 ...
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

    sa=i['sub_action']

    sdi=i.get('skip_device_init','')

    sca=i.get('skip_clean_after','')

    misc=i.get('misc',{})
    ccc=i.get('characteristics',{})
    env=i.get('env',{})
    deps=i.get('deps',{})

    ee=i.get('extra_env','')

    cons=i.get('console','')

    flags=i.get('flags','')
    lflags=i.get('lflags','')

    cv=i.get('compiler_vars',{})

    xrepeat=i.get('repeat','')
    if xrepeat=='': xrepeat='-1'
    repeat=int(xrepeat)

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')

    # Get some info about platforms
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'skip_device_init':sdi}

    if sa=='run': 
       ii['skip_info_collection']='no'
       ii['out']=o
    else:
       ii['skip_info_collection']='yes'

    r=ck.access(ii)
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    bhos=hosd.get('base_uid','')
    if bhos=='': bhos=hos
    bhosx=hosd.get('base_uoa','')
    if bhosx=='': bhosx=hosx
    btos=tosd.get('base_uid','')
    if btos=='': btos=tos
    btosx=tosd.get('base_uoa','')
    if btosx=='': btosx=tosx

    if r['device_id']!='': tdid=r['device_id']
    xtdid=''
    if tdid!='': xtdid=' -s '+tdid

    remote=tosd.get('remote','')

    tbits=tosd.get('bits','')

    # update misc
    misc['host_os_uoa']=hosx
    misc['target_os_uoa']=tosx
    misc['target_os_bits']=tbits
    misc['device_id']=tdid

    # Check compile type
    ctype=i.get('compile_type','')
    if i.get('static','')=='yes': ctype='static'
    if i.get('dynamic','')=='yes': ctype='dynamic'
    # On default Android-32, use static by default 
    # (old platforms has problems with dynamic)
    if ctype=='':
       if tosd.get('default_compile_type','')!='':
          ctype=tosd['default_compile_type']
       else:
          ctype='dynamic'

    # Get host platform type (linux or win)
    rx=ck.get_os_ck({})
    if rx['return']>0: return rx
    hplat=rx['platform']

    rem=hosd.get('rem','')
    eset=hosd.get('env_set','')
    etset=tosd.get('env_set','')
    svarb=hosd.get('env_var_start','')
    svarb1=hosd.get('env_var_extra1','')
    svare=hosd.get('env_var_stop','')
    svare1=hosd.get('env_var_extra2','')
    scall=hosd.get('env_call','')
    sdirs=hosd.get('dir_sep','')
    sdirsx=tosd.get('remote_dir_sep','')
    if sdirsx=='': sdirsx=sdirs
    stdirs=tosd.get('dir_sep','')
    sext=hosd.get('script_ext','')
    sexe=hosd.get('set_executable','')
    se=tosd.get('file_extensions',{}).get('exe','')
    sbp=hosd.get('bin_prefix','')
    stbp=tosd.get('bin_prefix','')
    sqie=hosd.get('quit_if_error','')
    evs=hosd.get('env_var_separator','')
    envsep=hosd.get('env_separator','')
    envtsep=tosd.get('env_separator','')
    eifs=hosd.get('env_quotes_if_space','')
    eifsc=hosd.get('env_quotes_if_space_in_call','')
    eifsx=tosd.get('remote_env_quotes_if_space','')
    if eifsx=='': eifsx=eifsc
    wb=tosd.get('windows_base','')
    stro=tosd.get('redirect_stdout','')
    stre=tosd.get('redirect_stderr','')
    ubtr=hosd.get('use_bash_to_run','')
    no=tosd.get('no_output','')

    ########################################################################
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
    if meta.get('skip_bin_ext','')!='yes':
       target_exe+=se

    # If muoa=='' assume program
    if muoa=='':
       muoa=work['self_module_uid']

    if duoa=='':
       x=meta.get('backup_data_uid','')
       if x!='':
          duoa=meta['backup_data_uid']

    # Reuse compile deps in run (useful for large benchmarks such as SPEC where compile and run is merged)
    rcd=meta.get('reuse_compile_deps_in_run','')

    # Check if compile in tmp dir
    cdir=p
    os.chdir(cdir)

    ##################################################################################################################
    ################################### Clean ######################################
    if sa=='clean':
       # Get host platform type (linux or win)
       cmd=cfg.get('clean_cmds',{}).get(hplat)

       if o=='con':
          ck.out(cmd)
          ck.out('')

       if ubtr!='': cmd=ubtr.replace('$#cmd#$',cmd)
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

    td=''
    if x=='yes':
       tdx=i.get('tmp_dir','')
       td=tdx
       if td=='': td='tmp'

       if i.get('clean','')=='yes':
          if td!='' and os.path.isdir(td):
             shutil.rmtree(td, ignore_errors=True)

       if tdx=='' and i.get('generate_rnd_tmp_dir','')=='yes':
          # Generate tmp dir
          import tempfile
          fd, fn=tempfile.mkstemp(suffix='', prefix='tmp-ck-')
          os.close(fd)
          os.remove(fn)
          td=os.path.basename(fn)

       cdir=os.path.join(p, td)

    misc['tmp_dir']=td
    misc['path']=p

    if cdir!='' and not os.path.isdir(cdir):
       os.mkdir(cdir)

    sb='' # Batch

    if o=='con':
       ck.out(sep)
       ck.out('Current directory: '+cdir)
       ck.out('')

    os.chdir(cdir)
    rcdir=os.getcwd()

    # If run and dynamic or reuse compile deps, check deps prepared by compiler
    fdeps=cfg.get('deps_file','')
    if len(deps)==0 and sa=='run' and (rcd=='yes' or ctype=='dynamic'):
       if os.path.isfile(fdeps):
          if o=='con':
             ck.out('')
             ck.out('Reloading depedencies from compilation '+fdeps+' ...')

          rx=ck.load_json_file({'json_file':fdeps})
          if rx['return']>0: return rx
          deps=rx['dict']

    # If compile type is dynamic, reuse deps even for run (to find specific DLLs) 
    # (REMOTE PLATFORMS ARE NOT SUPPORTED AT THE MOMENT, USE STATIC COMPILATION)
    if (ctype=='dynamic' or sa=='compile' or rcd=='yes'):
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
              'device_id':tdid,
              'deps':deps,
              'add_customize':'yes'}
          if o=='con': ii['out']='con'

          rx=ck.access(ii)
          if rx['return']>0: return rx

          if sa=='compile' or remote!='yes':
             sb+=no+rx['bat']

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

    ##################################################################################################################
    ################################### Compile ######################################
    if sa=='compile' or sa=='get_compiler_version':
       # Clean target file
       if target_exe!='' and os.path.isfile(target_exe):
          os.remove(target_exe)

       # Add compiler dep again, if there
       cb=deps.get('compiler',{}).get('bat','')
       if cb!='' and not sb.endswith(cb):
          sb+='\n'+no+cb+'\n'

       # Add env
       for k in sorted(env):
           v=env[k]

           if eifs!='' and wb!='yes':
              if v.find(' ')>=0 and not v.startswith(eifs):
                 v=eifs+v+eifs

           sb+=no+eset+' '+k+'='+v+'\n'
       sb+='\n'

       # Try to detect version
       csd=deps.get('compiler',{}).get('dict',{})
       csuoa=csd.get('soft_uoa','')
       if csuoa!='':
          r=ck.access({'action':'detect',
                       'module_uoa':cfg['module_deps']['soft'],
                       'uoa':csuoa,
                       'env':cb,
                       'con':o})
          if r['return']==0:
             cver=r['version_str']
             misc['compiler_detected_ver_list']=r['version_lst']
             misc['compiler_detected_ver_str']=cver
             misc['compiler_detected_ver_raw']=r['version_raw']

             if o=='con':
                ck.out('')
                ck.out('Detected compiler version: '+cver)
                ck.out('')

       if sa=='compile':
          # Check linking libs + include paths for deps
          sll=''
          sin=''
          for k in deps:
              kv=deps[k].get('cus',{})

              pl1=kv.get('path_lib','')
              pl2=kv.get('static_lib','')

              if pl2!='':
                 if ctype=='dynamic' and remote=='yes' and csd.get('customize',{}).get('can_strip_dynamic_lib','')=='yes':
                    pl2x=os.path.splitext(pl2)[0]
                    if pl2x.startswith('lib'): pl2x=pl2x[3:]
                    sll+=' '+svarb+svarb1+'CK_FLAG_PREFIX_LIB_DIR'+svare1+svare+eifsc+pl1+eifsc+' -l'+pl2x
   #                 sll+='/link /LIBPATH:'+eifsc+pl1+eifsc+' OpenCL.lib'

                 else:
                    if sll!='': sll+=' '
                    sll+=eifsc
                    if pl1!='': 
                       sll+=pl1+sdirs
                    sll+=pl2
                    sll+=eifsc

              pl3=kv.get('path_include','')
              if pl3!='':
                 if sin!='': sin+=' '
                 sin+=svarb+svarb1+'CK_FLAG_PREFIX_INCLUDE'+svare1+svare+eifsc+pl3+eifsc

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
          scfb+=' '+svarb+svarb1+'CK_FLAG_PREFIX_INCLUDE'+svare1+svare+sfprefix

          scfa=''

          # Check build -D flags
          sbcv=''
          bcv=meta.get('build_compiler_vars',{})
          bcv.update(cv)

          if o=='con' and len(bcv)>0:
             ck.out(sep)
             ck.out('Compiler vars:')

          for k in bcv:
              kv=bcv[k]
              if sbcv!='': sbcv+=' '
              sbcv+=svarb+svarb1+'CK_FLAG_PREFIX_VAR'+svare1+svare+k
              if kv!='': sbcv+='='+str(kv)

              if o=='con':
                 ck.out('  '+k+'='+str(kv))

          # Prepare compilation
          sb+='\n'

          denv=dcomp.get('env',{})
          sobje=denv.get('CK_OBJ_EXT','')
          sofs=''
          xsofs=[]

          if ee!='':
             sb+='\n'+no+ee+'\n\n'

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

              if 'CK_FLAGS_OUTPUT' in denv:
                 xcfa+=' '+svarb+svarb1+'CK_FLAGS_OUTPUT'+svare1+svare+sfobj

              cc=sccmd
              cc=cc.replace('$#source_file#$', sfprefix+sf)

              cc=cc.replace('$#compiler#$', svarb+compiler_env+svare)

              cc=cc.replace('$#flags_before#$', xcfb)
              cc=cc.replace('$#flags_after#$', xcfa)

              sb+='echo '+eifs+cc+eifs+'\n'
              sb+=no+cc+'\n'
              sb+=no+sqie+'\n'

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

                slfa=' '+svarb+svarb1+'CK_FLAGS_OUTPUT'+svare1+svare+target_exe
                slfa+=' '+svarb+'CK_LD_FLAGS_MISC'+svare
                slfa+=' '+svarb+'CK_LD_FLAGS_EXTRA'+svare

                if sll!='': slfa+=' '+sll

                evr=meta.get('extra_ld_vars','')
                if evr!='':
                   evr=evr.replace('$<<',svarb).replace('>>$',svare)
                   slfa+=' '+evr

                cc=slcmd
                cc=cc.replace('$#linker#$', svarb+linker_env+svare)
                cc=cc.replace('$#obj_files#$', sofs)
                cc=cc.replace('$#flags_before#$', slfb)
                cc=cc.replace('$#flags_after#$', slfa)

                sb+='echo '+eifs+cc+eifs+'\n'
                sb+=no+cc+'\n'
                sb+=no+sqie+'\n'

          # Try objdump
          sb+='\n'+no+svarb+'CK_OBJDUMP'+svare+' '+target_exe+' '+stro+' '+target_exe+'.dump'+'\n'
          sb+='\n'+no+'md5sum < '+target_exe+'.dump '+stro+' '+target_exe+'.md5'+'\n'

          # Record to tmp batch and run
          rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'yes'})
          if rx['return']>0: return rx
          fn=rx['file_name']

          rx=ck.save_text_file({'text_file':fn, 'string':sb})
          if rx['return']>0: return rx

          y=''
          if sexe!='':
             y+=sexe+' '+sbp+fn+envsep
          y+=' '+scall+' '+sbp+fn

          if o=='con':
             ck.out('')
             ck.out('Executing prepared batch file '+fn+' ...')
     
          sys.stdout.flush()
          start_time1=time.time()

          if ubtr!='': y=ubtr.replace('$#cmd#$',y)

          rx=os.system(y)
          comp_time=time.time()-start_time1

          ccc['compilation_time']=comp_time

          if sca!='yes':
             if fn!='' and os.path.isfile(fn): os.remove(fn)

          ofs=0
          md5=''
          if rx>0:
             misc['compilation_success']='no'
          else:
             misc['compilation_success']='yes'

             # Check some characteristics
             if os.path.isfile(target_exe):
                ccc['binary_size']=os.path.getsize(target_exe)

                # Try to read md5 file
                if os.path.isfile(target_exe+'.md5'):
                   rz=ck.load_text_file({'text_file':target_exe+'.md5'})
                   if rz['return']==0:
                      md5x=rz['string']
                      ix=md5x.find(' ')
                      if ix>0:
                         md5=md5x[:ix].strip()
                         ccc['md5_sum']=md5

             # Check obj file sizes
             if len(xsofs)>0:
                ccc['obj_sizes']={}
                for q in xsofs:
                    if os.path.isfile(q):
                       ofs1=os.path.getsize(q)
                       ccc['obj_sizes'][q]=ofs1
                       ofs+=ofs1
                ccc['obj_size']=ofs

          ccc['compilation_time_with_module']=time.time()-start_time

          if o=='con':
             ck.out('')
             ck.out('Compilation time: '+('%.3f'%comp_time)+' sec.; Object size: '+str(ofs)+'; MD5: '+md5)

    ##################################################################################################################
    ################################### Run ######################################
    elif sa=='run':
       start_time=time.time()

       sc=i.get('skip_calibration','')
       xcalibrate_time=i.get('calibration_time','')
       if xcalibrate_time=='': xcalibrate_time=cfg['calibration_time']
       calibrate_time=float(xcalibrate_time)

       # Update environment
       env1=meta.get('run_vars',{})
       for q in env1:
           if q not in env:
              env[q]=env1[q]

       # Update env if repeat
       if sc!='yes' and 'CT_REPEAT_MAIN' in env1:
          if repeat!=-1:
             if 'CT_REPEAT_MAIN' not in env1:
                return {'return':1, 'error':'this program is not supporting execution time calibration'}
             env['CT_REPEAT_MAIN']=str(repeat) # it is fixed by user
             sc='yes'
          else:
             repeat=int(env1.get('CT_REPEAT_MAIN','1'))
             env['CT_REPEAT_MAIN']='$#repeat#$' # find later

       # Check cmd key
       run_cmds=meta.get('run_cmds',{})
       if len(run_cmds)==0:
          return {'return':1, 'error':'no CMD for run'}

       krun_cmds=sorted(list(run_cmds.keys()))

       kcmd=i.get('cmd_key','')
       if kcmd=='':
          if len(krun_cmds)>1:
             ck.out('')
             ck.out('More than one commmand line is found to run this program:')
             ck.out('')
             zz={}
             iz=0
             for z in sorted(krun_cmds):
                 zs=str(iz)
                 zz[zs]=z

                 ck.out(zs+') '+z)

                 iz+=1

             ck.out('')
             rx=ck.inp({'text':'Choose first number to select command line: '})
             x=rx['string'].strip()

             if x not in zz:
                return {'return':1, 'error':'command line number is not recognized'}

             kcmd=zz[x]

          else:
             kcmd=krun_cmds[0]
       else:
          if kcmd not in krun_cmds:
             return {'return':1, 'error':'CMD key not found in program description'}

       # Command line key is set
       vcmd=run_cmds[kcmd]
       misc['cmd_key']=kcmd

       c=''

       rt=vcmd.get('run_time',{})

       rif=rt.get('run_input_files',[])
       rifo={}

       # Check if dynamic and remote to copy .so to devices
       if ctype=='dynamic' and remote=='yes':
          for q in deps:
              qq=deps[q].get('cus','')
              qdl=qq.get('dynamic_lib','')
              if qdl!='':
                 qpl=qq.get('path_lib','')
                 qq1=os.path.join(qpl,qdl)
                 rif.append(qq1)
                 rifo[qq1]='yes' # if pushing to external, do not use current path

       # Check if run_time env is also defined
       rte=rt.get('run_set_env2',{})
       if len(rte)>0:
          env.update(rte)

       # Add compiler dep again, if there
       x=deps.get('compiler',{}).get('bat','')
       if remote!='yes' and x!='' and not sb.endswith(x):
          sb+='\n'+no+x+'\n'

       # Add env
       sb+='\n'
       for k in sorted(env):
           v=env[k]

           if eifs!='' and wb!='yes':
              if v.find(' ')>=0 and not v.startswith(eifs):
                 v=eifs+v+eifs

           sb+=no+etset+' '+k+'='+v+'\n'
       sb+='\n'

       if tosd.get('extra_env','')!='':
          sb+=no+tosd['extra_env']+'\n'

       # Command line preparation
       c=rt.get('run_cmd_main','')
       if c=='':
          return {'return':1, 'error':'cmd is not defined'}
       c=c.replace('$<<',svarb+svarb1).replace('>>$',svare1+svare)

       # Remote dir
       if remote=='yes':
          rdir=tosd.get('remote_dir','')
          if rdir!='' and not rdir.endswith(stdirs): rdir+=stdirs

       # Replace bin file
       te=target_exe
       if meta.get('skip_add_prefix_for_target_file','')!='yes':
          te=stbp+te

       c=c.replace('$#BIN_FILE#$', te)
       c=c.replace('$#os_dir_separator#$', stdirs)
       if remote=='yes':
          c=c.replace('$#src_path#$', rdir+stdirs)
       else:
          c=c.replace('$#src_path#$', p+sdirs)

       c=c.replace('$#env1#$',svarb)
       c=c.replace('$#env2#$',svare)

       # Check if takes datasets from CK
       dtags=vcmd.get('dataset_tags',[])
       dmuoa=cfg['module_deps']['dataset']
       dduoa=i.get('dataset_uoa','')
       if dduoa!='' or len(dtags)>0:
          if dduoa=='':
             misc['dataset_tags']=dtags

             tags=''
             for q in dtags:
                 if tags!='': tags+=','
                 tags+=q

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
                ck.out('')
                ck.out('More than one dataset entry is found for this program:')
                ck.out('')
                zz={}
                iz=0
                for z1 in sorted(lst, key=lambda v: v['data_uoa']):
                    z=z1['data_uid']
                    zu=z1['data_uoa']

                    zs=str(iz)
                    zz[zs]=z

                    ck.out(zs+') '+zu+' ('+z+')')

                    iz+=1

                ck.out('')
                rx=ck.inp({'text':'Choose first number to select dataset UOA: '})
                x=rx['string'].strip()

                if x not in zz:
                   return {'return':1, 'error':'dataset number is not recognized'}

                dduoa=zz[x]

          if dduoa=='':
             return {'return':1, 'error':'dataset is not specified'}  

       misc['dataset_uoa']=dduoa

       # If remote
       if remote=='yes':
          if target_exe=='':
             return {'return':1, 'error':'currently can\'t run benchmarks without defined executable on remote platform'}

          rs=tosd['remote_shell'].replace('$#device#$',xtdid)
          rse=tosd.get('remote_shell_end','')+' '

          if sdi!='yes':
             ck.out(sep)
             r=ck.access({'action':'init_device',
                          'module_uoa':cfg['module_deps']['platform'],
                          'os_dict':tosd,
                          'device_id':tdid,
                          'out':o})
             if r['return']>0: return r

          if i.get('statistical_repetition',0)==0:
             # Copy exe
             y=tosd.get('remote_push_pre','').replace('$#device#$',xtdid)
             if y!='':
                y=y.replace('$#file1#$', target_exe)
                y=y.replace('$#file1s#$', target_exe)
                y=y.replace('$#file2#$', rdir+target_exe)

                if o=='con':
                   ck.out(sep)
                   ck.out(y)
                   ck.out('')

                ry=os.system(y)
                if ry>0:
                   return {'return':1, 'error':'copying to remote device failed'}

             y=tosd['remote_push'].replace('$#device#$',xtdid)
             y=y.replace('$#file1#$', target_exe)
             y=y.replace('$#file1s#$', target_exe)
             y=y.replace('$#file2#$', rdir+target_exe)

             if o=='con':
                ck.out(sep)
                ck.out(y)
                ck.out('')

             ry=os.system(y)
             if ry>0:
                return {'return':1, 'error':'copying to remote device failed'}

             # Set chmod
             se=tosd.get('set_executable','')
             if se!='':
                y=rs+' '+se+' '+rdir+target_exe+' '+rse
                if o=='con':
                   ck.out(sep)
                   ck.out(y)
                   ck.out('')

                ry=os.system(y)
                if ry>0:
                   return {'return':1, 'error':'making binary executable failed on remote device'}

          if sdi!='yes':
             # Copy explicit input files, if first time
             for df in rif:
                 df0, df1 = os.path.split(df)

                 # Push data files to device
                 y=tosd.get('remote_push_pre','').replace('$#device#$',xtdid)
                 if y!='':
                    if df in rifo:
                       dfx=df
                       dfy=rdir+stdirs+df1
                    else:
                       dfx=os.path.join(p,df)
                       dfy=rdir+stdirs+df

                    y=y.replace('$#file1#$', dfx)
                    y=y.replace('$#file1s#$', df1)
                    y=y.replace('$#file2#$', dfy)

                    if o=='con':
                       ck.out(sep)
                       ck.out(y)
                       ck.out('')

                    ry=os.system(y)
                    if ry>0:
                       return {'return':1, 'error':'copying to remote device failed'}

                 y=tosd['remote_push'].replace('$#device#$',xtdid)
                 y=y.replace('$#file1#$', dfx)
                 y=y.replace('$#file1s#$', df1)
                 y=y.replace('$#file2#$', dfy)
                 if o=='con':
                    ck.out(sep)
                    ck.out(y)
                    ck.out('')

                 ry=os.system(y)
                 if ry>0:
                    return {'return':1, 'error':'copying to remote device failed'}

       # Loading dataset
       if dduoa!='':
          rx=ck.access({'action':'load',
                        'module_uoa':dmuoa,
                        'data_uoa':dduoa})
          if rx['return']>0: return rx
          dd=rx['dict']
          dp=rx['path']

          if remote=='yes':
             c=c.replace('$#dataset_path#$','')
          else:
             c=c.replace('$#dataset_path#$',dp+sdirs)

          dfiles=dd.get('dataset_files',[])
          if len(dfiles)>0:
             for k in range(0, len(dfiles)):
                 df=dfiles[k]
                 kk='$#dataset_filename'
                 if k>0: kk+='_'+str(k)
                 kk+='#$'
                 c=c.replace(kk, df)

                 if remote=='yes' and sdi!='yes':
                    df0, df1 = os.path.split(df)

                    # Push data files to device
                    y=tosd.get('remote_push_pre','').replace('$#device#$',xtdid)
                    if y!='':
                       y=y.replace('$#file1#$', os.path.join(dp,df))
                       y=y.replace('$#file1s#$', df1)
                       y=y.replace('$#file2#$', rdir+stdirs+df)

                       if o=='con':
                          ck.out(sep)
                          ck.out(y)
                          ck.out('')

                       ry=os.system(y)
                       if ry>0:
                          return {'return':1, 'error':'copying to remote device failed'}

                    # Push data files to device, if first time
                    y=tosd['remote_push'].replace('$#device#$',xtdid)
                    y=y.replace('$#file1#$', os.path.join(dp,df))
                    y=y.replace('$#file1s#$', df1)
                    y=y.replace('$#file2#$', rdir+stdirs+df)
                    if o=='con':
                       ck.out(sep)
                       ck.out(y)
                       ck.out('')

                    ry=os.system(y)
                    if ry>0:
                       return {'return':1, 'error':'copying to remote device failed'}

          rcm=dd.get('cm_properties',{}).get('run_time',{}).get('run_cmd_main',{})
          for k in rcm:
              kv=rcm[k]
              c=c.replace('$#'+k+'#$',kv)

          misc['dataset_uoa']=dduoa

       # Check if redirect output
       rco1=rt.get('run_cmd_out1','')
       rco2=rt.get('run_cmd_out2','')

       if ee!='':
          sb+='\n'+no+ee+'\n\n'

       if remote!='yes' and cons!='yes':
          if rco1!='': c+=' '+stro+' '+rco1
          if rco2!='': c+=' '+stre+' '+rco2
       sb+=no+c+'\n'

       fn=''

       fgtf=rt.get('fine_grain_timer_file','')

       # Calibrate execution time (to make it longer and minimize system variation, 
       #   if supported)
       csb=sb
       orepeat=repeat
       calibrate_success=False

       xcn_max=i.get('calibration_max','')
       if xcn_max=='': xcn_max=cfg['calibration_max']
       cn_max=int(xcn_max)

       cn=1
       while True:
          # Clean output files
          rof=rt.get('run_output_files',[])
          for df in rof:
              if remote=='yes':
                 # Clean data files on device
                 y=rs+' '+tosd['delete_file']+ ' '+rdir+stdirs+df+' '+rse
                 if o=='con':
                    ck.out('')
                    ck.out(y)
                    ck.out('')

                 ry=os.system(y)

                 if tosd.get('delete_file_extra','')!='':
                    y=tosd['delete_file_extra']+df+' '+rse
                    if o=='con':
                       ck.out('')
                       ck.out(y)
                       ck.out('')

                    ry=os.system(y)

              if os.path.isfile(df): 
                 os.remove(df)

          if sc!='yes' and 'CT_REPEAT_MAIN' in env1:
             if o=='con':
                ck.out('')
                ck.out('### Calibration '+str(cn)+' out of '+xcn_max+' ; Kernel repeat number = '+str(repeat))

          sb=csb
          if sc!='yes' and 'CT_REPEAT_MAIN' in env1 and repeat!=-1:
             sb=sb.replace('$#repeat#$', str(repeat))

          # Prepare execution
          if o=='con':
             ck.out(sep)

          if remote=='yes':
             # Prepare command as one line
             y=''

             x=sb.split('\n')
             for q in x:
                 if q!='':
                    if y!='': y+=envtsep
                    y+=' '+q

             if eifsx!='': y=y.replace('"','\\"')
             y=rs+' '+eifsx+tosd['change_dir']+' '+rdir+envtsep+' '+y+eifsx+' '+rse

             if cons!='yes':
                if rco1!='': y+=' '+stro+' '+rco1
                if rco2!='': y+=' '+stre+' '+rco2

             if o=='con':
                ck.out(y)

          else:
             # Record to tmp batch and run
             rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'yes'})
             if rx['return']>0: return rx
             fn=rx['file_name']

             rx=ck.save_text_file({'text_file':fn, 'string':sb})
             if rx['return']>0: return rx

             y=''
             if sexe!='':
                y+=sexe+' '+sbp+fn+envsep
             y+=' '+scall+' '+sbp+fn

             if o=='con':
                ck.out(sb)
                ck.out('')
                ck.out(' ('+y+')')

          if remote!='yes' and ubtr!='': y=ubtr.replace('$#cmd#$',y)

          if o=='con':
             ck.out('')

          sys.stdout.flush()
          start_time1=time.time()
          rx=os.system(y)
          exec_time=time.time()-start_time1

          if sca!='yes':
             if fn!='' and os.path.isfile(fn): os.remove(fn)

          # Pull files from the device if remote
          if remote=='yes':
             rof=rt.get('run_output_files',[])

             xrof=rof
             if i.get('pull_only_timer_files','')=='yes':
                xrof=[fgtf]
 
             for df in xrof:
                 # Pull output files from device
                 df0, df1 = os.path.split(df)

                 # Push data files to device
                 y=tosd['remote_pull'].replace('$#device#$',xtdid)
                 y=y.replace('$#file1#$', rdir+stdirs+df)
                 y=y.replace('$#file1s#$', df1)
                 y=y.replace('$#file2#$', df)
                 if o=='con':
                    ck.out('')
                    ck.out(y)
                    ck.out('')

                 ry=os.system(y)

                 y=tosd.get('remote_pull_post','').replace('$#device#$',xtdid)
                 if y!='':
                    y=y.replace('$#file1#$', rdir+stdirs+df)
                    y=y.replace('$#file1s#$', df1)
                    y=y.replace('$#file2#$', df)

                    if o=='con':
                       ck.out(sep)
                       ck.out(y)
                       ck.out('')

                    ry=os.system(y)
                    if ry>0:
                       return {'return':1, 'error':'pulling from remote device failed'}

          # Check if fine-grain time
          if fgtf!='':
             if o=='con':
                ck.out('')
                ck.out('Reading fine grain timers from '+fgtf+' ...')
                ck.out('')

             rq=ck.load_json_file({'json_file':fgtf})
             if rq['return']>0: return rq
             drq=rq['dict']
             ccc.update(drq)
             et=drq.get('execution_time','')
             exec_time=0.0
             if et!='':
                exec_time=float(et)

          # If return code >0 and program does not ignore return code, quit
          if rx>0 and vcmd.get('ignore_return_code','').lower()!='yes':
             break

          # Check calibration
          if sc=='yes' or repeat==-1 or 'CT_REPEAT_MAIN' not in env1:
             calibrate_success=True
             break

          orepeat=repeat
          if exec_time<0.5: repeat*=10
          elif 0.8<(calibrate_time/exec_time)<1.4: 
             calibrate_success=True
             break
          else: 
             repeat*=float(calibrate_time/exec_time)
             if repeat<1: repeat=1
          repeat=int(repeat)

          if repeat==orepeat:
             calibrate_success=True
             break

          if o=='con' and sc!='yes':
             ck.out('')
             ck.out('### Calibration: time='+str(exec_time)+'; CT_REPEAT_MAIN='+str(orepeat)+'; new CT_REPEAT_MAIN='+str(repeat))

          if cn>=cn_max:
             return {'return':1, 'error':'calibration failed'}

          cn+=1

       if sc!='yes' and repeat!=-1:
          if calibrate_success==False:
             return {'return':1, 'error':'calibration problem'}

       xrepeat=repeat
       if xrepeat<1: xrepeat=1

       ccc['return_code']=rx
       ccc['execution_time']=exec_time/repeat
       ccc['total_execution_time']=exec_time
       ccc['repeat']=xrepeat
       misc['calibration_success']=calibrate_success

       if rx>0 and vcmd.get('ignore_return_code','').lower()!='yes':
          misc['run_success']='no'
       else:
          misc['run_success']='yes'

       ccc['execution_time_with_module']=time.time()-start_time

       if o=='con':
          ck.out('')
          x='Execution time: '+('%.3f'%exec_time)
          if repeat>1:
             x+=' sec.; Repetitions: '+str(repeat)+'; Normalized execution time: '+('%.9f'%(exec_time/repeat))+' sec.'
          ck.out(x)

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
# non-universal (traditional) program compiler flag autotuning

def autotune(i):
    """
    Input:  {
              (repo_uoa)   - program repo UOA
              (module_uoa) - program module UOA
              data_uoa     - program data UOA

              (host_os)        - host OS (detect, if omitted)
              (target_os)      - OS module to check (if omitted, analyze host)
              (device_id)      - device id if remote (such as adb)

              (process_in_tmp)
              (tmp_dir)

              (cmd_key)
              (dataset_uoa)

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

    # Prepare copy of input to reuse later
    ic=copy.deepcopy(i)

    pp=os.getcwd()

    ni=i.get('number_of_iterations',0)
    try: ni=int(ni)
    except Exception as e: pass

    srm=i.get('stat_repetitions',0)
    try: srm=int(srm)
    except Exception as e: pass

    deps={}

    cmd_key=i.get('cmd_key','')
    dduoa=i.get('dataset_uoa','')

    dflag=i.get('default_flag','')

    eruoa=i.get('experiment_repo_uoa','')
    euoa=i.get('experiment_uoa','')

    tdid=i.get('device_id','')

    # Hack
    cduoa=i.get('compiler_desc_uoa','')
    if cduoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['compiler'],
                     'data_uoa':cduoa})
       if rx['return']>0: return rx
       cm=rx['dict']
       cc=cm.get('all_compiler_flags_desc',{})

    sdi='no'

    for m in range(0,ni+1):
        grtd=i.get('generate_rnd_tmp_dir','')
        if grtd=='': grtd='yes'
        tmp_dir=i.get('tmp_dir','')

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
        # Compile 
        os.chdir(pp)

        if grtd=='yes':
           ii['generate_rnd_tmp_dir']='yes'
        else:
           ii['generate_rnd_tmp_dir']=''

        if tdid!='': ii['device_id']=tdid

        ck.out('')

        rx=compile(ii)  #####################################################################
        if rx['return']>0: return rx 

        deps=rx['deps']
        cmisc=rx['misc']
        cch=rx['characteristics']

        if cmisc.get('device_id','')!='': tdid=cmisc['device_id']

        tmp_dir=cmisc['tmp_dir']
        tp=cmisc['path']

        xct=cch.get('compilation_time',-1)
        xos=cch.get('obj_size',-1)

        dd['characteristics']['compile']=cch
        dd['misc']['compile']=cmisc

        if xos>0:
           ##########################################################################################
           # Run
           ii['deps']=deps
           ii1=copy.deepcopy(ii)

           repeat=-1

           for sr in range(0, srm):
               ck.out('')
               ck.out('------------------- Statistical reptition: '+str(sr))
               ii=copy.deepcopy(ii1)

               os.chdir(pp)

               ii['skip_device_init']=sdi

               ii['statistical_repetition']=sr # Needed to avoid pushing a.out to remote device

               if repeat!=-1:
                  ii['repeat']=repeat

               if tmp_dir!='':
                  ii['tmp_dir']=tmp_dir

               if cmd_key!='':
                  ii['cmd_key']=cmd_key

               if dduoa!='':
                  ii['dataset_uoa']=dduoa

               if tdid!='':
                  ii['device_id']=tdid

               if repeat!=-1:
                  ii['pull_only_timer_files']='yes'

               rx=run(ii)  ###############################################################
               if rx['return']>0: return rx

               if sdi!='yes': sdi='yes'

               rmisc=rx['misc']
               rch=rx['characteristics']

               if rmisc.get('device_id','')!='': tdid=rmisc['device_id']

               cmd_key=rmisc.get('cmd_key','')
               dduoa=rmisc.get('dataset_uoa','')

               rsucc=rmisc.get('run_success','')
               dataset_uoa=rmisc.get('dataset_uoa','')
               xrt=rch.get('execution_time',-1)

               repeat=rch.get('repeat',-1)
               xnrt=rch.get('normalized_execution_time',-1)

               if rsucc=='yes' and xrt>0:
                  ck.out('')
                  ck.out('###### Compile time: '+str(xct)+', obj size: '+str(xos)+', run time: '+str(xrt)+', repeat: '+str(repeat))
                  ck.out('')

               dd['characteristics']['run']=rch
               dd['misc']['run']=rmisc

               ##########################################################################################
               # For now Process/record in expeirment, only if compile was successful
               # TBD: For compiler/architecture testing purposes, we may want to record failed cases in another repo

               ck.out(sep)

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

        if tmp_dir!='' and tmp_dir!='tmp' and i.get('skip_clean_after','')!='yes':
           os.chdir(tp)
           import shutil
           shutil.rmtree(tmp_dir)

    # Deinit remote device, if needed
    r=ck.access({'action':'deinit',
                 'module_uoa':cfg['module_deps']['platform'],
                 'host_os':i.get('host_os',''),
                 'target_os':i.get('target_os',''),
                 'device_id':i.get('device_id','')})
    if r['return']>0: return r

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

##############################################################################
# prepare and run program pipeline (clean, compile, run, etc)

def pipeline(i):
    """
    Input:  {
              (repo_uoa)             - program repo UOA
              (module_uoa)           - program module UOA
              (data_uoa)             - program data UOA
                 or
              (program_uoa)
                 or taken from .cm/meta.json from current directory

              (program_tags)         - select programs by these tags

              (program_dir)          - force program directory

              (host_os)              - host OS (detect, if omitted)
              (target_os)            - OS module to check (if omitted, analyze host)
              (device_id)            - device id if remote (such as adb)

              (prepare)              - if 'yes', only prepare setup, but do not clean/compile/run program
              (save_to_file)         - if !='', save updated input/output (state) to this file
              (skip_interaction)     - if 'yes' and out=='con', skip interaction to choose parameters

              (skip_device_init)     - if 'yes', skip device init
              (skip_info_collection) - if 'yes', skip info collection
                                 
                 Pipeline sections' settings:

              (no_platform_features) - do not collect full platform features
              (no_clean)             - do not clean directory before compile/run
              (no_compile)           - do not compile program
              (no_run)               - do not run program

              (generate_rnd_tmp_dir) - if 'yes', compile and run program in randomly generated temporal dir
                      or
              (tmp_dir)              - if !='', use this tmp_dir

              (skip_clean_after)     - if 'yes', do not remove run batch

              (console)              - if 'yes', output from program goes to console rather than file
                                          (usually for testing/demos)

              (cmd_key)
              (dataset_uoa)

              (compile_type)         - static or dynamic (dynamic by default;
                                         however takes compiler default_compile_type into account)
                  or
              (static or dynamic)

              (compiler_desc_uoa)    - compiler description UOA (module compiler),
                                       if not set, there will be an attempt to detect the most close
                                       by version

              (compiler_vars)        - dict with set up compiler flags (-Dvar=value) -> 
                                       they will update the ones defined as default in program description ...

              (flags)                - compile flags
              (lflags)               - link flags

              (env)                  - preset environment
              (extra_env)            - extra environment as string

              (repeat)               - repeat kernel via environment CT_REPEAT_MAIN if supported
              (skip_calibration)     - if 'yes', skip execution time calibration (make it around 4.0 sec)
              (calibration_time)     - calibration time in string, 4.0 sec. by default
              (calibration_max)      - max number of iterations for calibration, 10 by default

              (compile_deps)         - compilation dependencies

              (choices)              - exposed choices (if any)

              (features)             - exposed features (if any)

              (characteristics)      - measured characteristics/features/properties (if any)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              !!! The same as input, but with updated information !!!

              ready        - if 'yes', pipeline is ready (all obligatory choices are set)
                             if 'no', clean/compile/run program is postponed

              (tmp_dir)    - if temporal directory is used, return it 
                             (useful if randomly generated, to be reused for run or further iterations)


            }

    """

    import os
    import copy
    import json

    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    pr=i.get('prepare','')
    si=i.get('skip_interaction','')

    if 'tmp' not in i: i['tmp']={}
    tmp=i['tmp']

    tmp['cur_dir']=os.getcwd()

    if 'choices_desc' not in i: i['choices_desc']={}
    choices=i['choices_desc']

    if 'features' not in i: i['features']={}
    features=i['features']

    if 'characteristics' not in i: i['characteristics']={}
    chars=i['characteristics']

    i['ready']='no'
    i['fail']='no'

    ###############################################################################################################
    # PIPELINE SECTION: VARS INIT

    if o=='con':
       ck.out('Initializing universal program pipeline ...')
       ck.out('')

    muoa=work['self_module_uid']

    meta=i.get('program_meta',{}) # program meta

    ruoa=i.get('repo_uoa','')
    duoa=i.get('data_uoa','')
    ptags=i.get('program_tags','')
    kcmd=i.get('cmd_key','')
    dduoa=i.get('dataset_uoa','')

    cdeps=i.get('compile_deps',{})

    pdir=i.get('program_dir','')
    if pdir!='': os.chdir(pdir)

    sdi=i.get('skip_device_init','')
    sic=i.get('skip_info_collection','')

    grtd=i.get('generate_rnd_tmp_dir','')
    tdir=i.get('tmp_dir','')
    sca=i.get('skip_clean_after','')

    flags=i.get('flags','')
    lflags=i.get('lflags','')

    env=i.get('env',{})
    eenv=i.get('extra_env','')

    repeat=i.get('repeat','')
    rsc=i.get('skip_calibration','')
    rct=i.get('calibration_time','')
    rcm=i.get('calibration_max','')

    cons=i.get('console','')

    ###############################################################################################################
    # PIPELINE SECTION: Host and target platform selection
    if o=='con':
       ck.out(sep)
       ck.out('Obtaining platform parameters and checking other obligatory choices for the pipeline ...')
       ck.out('')

    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tbits=i.get('target_os_bits','')
    tdid=i.get('device_id','')

    # Get some info about platforms
    ox=o
    if sdi=='yes' and sic=='yes': ox=''
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'skip_device_init':sdi,
        'skip_info_collection':sic,
        'out':ox}
    if si=='yes': ii['return_multi_devices']='yes'
    r=ck.access(ii)
    if r['return']>0: 
       if r['return']==32:
          choices['##device_id']={'type':'text',
                                  'has_choice':'yes',
                                  'choices':r['devices'],
                                  'tags':['setup'],
                                  'sort':1000}
          return finalize_pipeline(i)
       return r

    sdi='yes'
    i['skip_device_init']=sdi

    hos=r['host_os_uoa']
    hosd=r['host_os_dict']

    i['host_os']=hos

    tos=r['os_uoa']
    tosd=r['os_dict']
    tbits=tosd.get('bits','')

    hosz=hosd.get('base_uoa','')
    if hosz=='': hosz=hos
    tosz=tosd.get('base_uoa','')
    if tosz=='': tosz=tos

    remote=tosd.get('remote','')

    tdid=r['device_id']
    if tdid!='': i['device_id']=tdid

    i['target_os']=tos
    i['target_os_bits']=tbits

    i['device_id']=r['device_id']

    if hos=='':
       return {'return':1, 'error':'host_os is not defined'}

    if tos=='':
       return {'return':1, 'error':'target_os is not defined'}

    # Check compile type
    ctype=i.get('compile_type','')
    if i.get('static','')=='yes': ctype='static'
    if i.get('dynamic','')=='yes': ctype='dynamic'
    # On default Android-32, use static by default 
    # (old platforms has problems with dynamic)
    if ctype=='':
       if tosd.get('default_compile_type','')!='':
          ctype=tosd['default_compile_type']
       else:
          ctype='dynamic'
    i['compile_type']=ctype
        
    if o=='con':
       ck.out(sep)
       ck.out('  Selected host platform: '+hos)
       ck.out('  Selected target platform: '+tos)
       if tdid!='':
          ck.out('  Selected target device ID: '+tdid)

    ###############################################################################################################
    # PIPELINE SECTION: PROGRAM AND DIRECTORY SELECTION 
    #                   (either as CID or CK descrpition from current directory or return that should be selected)

    # First, if duoa is not defined, try to get from current directory
    if len(meta)==0:
       if duoa=='':
          # First, try to detect CID in current directory
          r=ck.cid({})
          if r['return']==0:
             xruoa=r.get('repo_uoa','')
             xmuoa=r.get('module_uoa','')
             xduoa=r.get('data_uoa','')

             rx=ck.access({'action':'load',
                           'module_uoa':xmuoa,
                           'data_uoa':xduoa,
                           'repo_uoa':xruoa})
             if rx['return']>0: return rx
             xmeta=rx['dict']

             if xmeta.get('program','')=='yes':
                duoa=xduoa
                muoa=xmuoa
                ruoa=xruoa
                meta=xmeta

          if duoa=='':
             # Attempt to load configuration from the current directory
             pc=os.path.join(tmp['cur_dir'], ck.cfg['subdir_ck_ext'], ck.cfg['file_meta'])
             if os.path.isfile(pc):
                r=ck.load_json_file({'json_file':pc})
                if r['return']==0:
                   xmeta=r['dict']
                   if xmeta.get('program','')=='yes':
                      meta=xmeta

    # Second, if duoa is not detected ordefined, prepare selection 
    duid=''
    if len(meta)==0:
       if duoa=='': duoa='*'

       r=ck.search({'repo_uoa':ruoa, 'module_uoa':muoa, 'data_uoa':duoa, 'add_info':'yes', 'tags':ptags})
       if r['return']>0: return r

       lst=r['lst']
       if len(lst)==0:
          duoa=''
       elif len(lst)==1:
          duid=lst[0]['data_uid']
          duoa=lst[0]['data_uoa']
       else:
          # SELECTOR *************************************
          choices['##program_uoa']={'type':'uoa',
                                    'has_choice':'yes',
                                    'choices':lst,
                                    'tags':['setup'],
                                    'sort':1000}

          if o=='con' and si!='yes':
             r=select_uoa({'choices':lst})
             if r['return']>0: return r
             duoa=r['choice']
             ck.out('')
          else:
             return finalize_pipeline(i)

    if len(meta)==0 and duoa=='':
       return {'return':0, 'error':'no programs found for this pipeline'}

    if pdir=='' and duoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':muoa,
                     'data_uoa':duoa,
                     'repo_uoa':ruoa})
       if rx['return']>0: return rx
       if len(meta)==0: 
          meta=rx['dict']
       pdir=rx['path']
       duid=rx['data_uid']
       duoa=rx['data_uoa']

    if pdir=='': pdir=tmp['cur_dir']

    i['program_meta']=meta

    if duid=='' and meta.get('backup_data_uid','')!='': duid=meta['backup_data_uid']

    if duoa!='': i['data_uoa']=duoa
    if muoa!='': i['module_uoa']=muoa
    # we are not recording repo_uoa for reproducibility (can be different across users) ...   

    if o=='con':
       ck.out('  Selected program: '+duoa+' ('+duid+')')

    ###############################################################################################################
    # PIPELINE SECTION: Command line selection 

    run_cmds=meta.get('run_cmds',{})
    if len(run_cmds)==0:
       return {'return':1, 'error':'no CMD for run'}

    krun_cmds=sorted(list(run_cmds.keys()))
    if kcmd=='':
       if len(krun_cmds)>1:
          xchoices=[]
          for z in sorted(krun_cmds):
              xchoices.append(z)

          # SELECTOR *************************************
          choices['##cmd_key']={'type':'text',
                                'has_choice':'yes',
                                'choices':xchoices,
                                'tags':['setup'],
                                'sort':1100}

          if o=='con' and si!='yes':
             ck.out('************ Selecting command line ...')
             ck.out('')
             r=select_list({'choices':xchoices})
             if r['return']>0: return r
             kcmd=r['choice']
             ck.out('')
          else:
             return finalize_pipeline(i)

       else:
          kcmd=krun_cmds[0]
    else:
       if kcmd not in krun_cmds:
          return {'return':1, 'error':'CMD key "'+kcmd+'" not found in program description'}

    i['cmd_key']=kcmd

    if o=='con':
       ck.out('  Selected command line: '+kcmd)

    ###############################################################################################################
    # PIPELINE SECTION: Command line selection 

    vcmd=run_cmds[kcmd]

    dtags=vcmd.get('dataset_tags',[])
    dmuoa=cfg['module_deps']['dataset']
    dduid=''

    if dduoa!='' or len(dtags)>0:
       if dduoa=='':
          xdtags=''
          for q in dtags:
              if xdtags!='': xdtags+=','
              xdtags+=q

          rx=ck.access({'action':'search',
                        'module_uoa':dmuoa,
                        'tags':xdtags})
          if rx['return']>0: return rx

          lst=rx['lst']

          if len(lst)==0:
             duoa=''
          elif len(lst)==1:
             dduid=lst[0]['data_uid']
             dduoa=lst[0]['data_uoa']
          else:
             # SELECTOR *************************************
             choices['##dataset_uoa']={'type':'uoa',
                                       'has_choice':'yes',
                                       'choices':lst,
                                       'tags':['setup', 'dataset'],
                                       'sort':1200}

             if o=='con' and si!='yes':
                ck.out('************ Selecting data set ...')
                ck.out('')
                r=select_uoa({'choices':lst})
                if r['return']>0: return r
                dduoa=r['choice']
                ck.out('')
             else:
                return finalize_pipeline(i)

       if dduoa=='':
          return {'return':1, 'error':'no datasets found for this pipeline'}

    if dduoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':dmuoa,
                     'data_uoa':dduoa})
       if rx['return']>0: return rx
       ddmeta=rx['dict']
       dduid=rx['data_uid']
       dduoa=rx['data_uoa']

    if dduoa!='': 
       i['dataset_uoa']=dduoa

       if o=='con':
          ck.out('  Selected data set: '+dduoa+' ('+dduid+')')

    ###############################################################################################################
    # PIPELINE SECTION: resolve compile dependencies 
    cdeps=i.get('compile_deps',{})
    if len(cdeps)==0: 
       cdeps=meta.get('compile_deps',{})

       if len(cdeps)>0:
          if o=='con':
             ck.out(sep)

          ii={'action':'resolve',
              'module_uoa':cfg['module_deps']['env'],
              'host_os':hos,
              'target_os':tos,
              'device_id':tdid,
              'deps':cdeps,
              'add_customize':'yes',
              'out':oo}

          rx=ck.access(ii)
          if rx['return']>0: return rx

          cdeps=rx['deps'] # Update deps (add UOA)
          i['compile_deps']=cdeps
    else:
       if o=='con':
          ck.out('  Selected dependencies: ')
          for dp in cdeps:
              dpx=cdeps[dp]
              tags=dpx.get('dict',{}).get('tags',[])
              x=json.dumps(tags, sort_keys=True)
              y=dpx.get('uoa','')
              ck.out('      '+dp+' env = '+y+'; tags = '+x)

    ###############################################################################################################
    # PIPELINE SECTION: Detect compiler version
    if i.get('no_detect_compiler_version','')!='yes':
       if o=='con':
          ck.out(sep)
          ck.out('Detect compiler version ...')
          ck.out('')

       if meta.get('no_compile','')!='yes':
          ii={'sub_action':'get_compiler_version',
              'host_os':hos,
              'target_os':tos,
              'deviced_id':tdid,
              'path':pdir,
              'meta':meta,
              'deps':cdeps,
              'generate_rnd_tmp_dir':grtd,
              'tmp_dir':tdir,
              'skip_clean_after':sca,
              'compile_type':ctype,
              'flags':flags,
              'lflags':lflags,
              'console':cons,
              'env':env,
              'extra_env':eenv,
              'out':oo}
          r=process_in_dir(ii)
          if r['return']>0: return r

          misc=r['misc']
          tdir=misc.get('tmp_dir','')
          if tdir!='': i['tmp_dir']=tdir



          features['compiler_version']={'list':misc.get('compiler_detected_ver_list',[]),
                                        'str':misc.get('compiler_detected_ver_str',''),
                                        'raw':misc.get('compiler_detected_ver_raw','')}



    ###############################################################################################################
    # PIPELINE SECTION: get compiler description for flag options
    cflags_desc=choices.get('##compiler_flags',{})

    cdu=i.get('compiler_description_uoa','')
    if cdu=='' and i.get('no_compiler_description','')!='yes':
       cdt=cdeps.get('compiler',{}).get('dict',{}).get('tags',[])

       # Substitute with real compiler version
       creal=features.get('compiler_version',{}).get('list',[])
       if len(creal)>0:
          cdt1=[]
          for q in cdt:
              if not q.startswith('v'): cdt1.append(q)
          qq=''
          for q in creal:
              if qq=='': qq='v'
              else: qq+='.'
              qq+=q
              cdt1.append(qq)

          # Find most close
          ii={'action':'list',
              'module_uoa':cfg['module_deps']['compiler'],
              'add_meta':'yes'}
          rx=ck.access(ii)
          if rx['return']>0: return rx

          rl=rx['lst']

          xrmax=0 # max tag matches
          xruid=''
          xruoa=''

          for q in rl:
              qdt=q.get('meta',{}).get('tags',[])
              rx=0
              for qi in cdt1:
                  if qi in qdt:
                     rx+=1
              if rx>xrmax:
                 xrmax=rx
                 xruid=q['data_uid']
                 xruoa=q['data_uoa']

          if xrmax==0:
             import json
             return {'return':1, 'error':'can\'t find most close compiler description by tags ('+json.dumps(cdt1)+')'}

          cdu=xruoa

          if o=='con':
             ck.out('')
             ck.out('Most close found compiler description: '+xruoa+' ('+xruid+')')

    if cdu!='':
       rx=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['compiler'],
                     'data_uoa':cdu})
       if rx['return']>0: return rx
       rxd=rx['dict']

       if len(cflags_desc)==0:
          cflags_desc=rxd.get('all_compiler_flags_desc',{})

          for q in cflags_desc:
              qq=cflags_desc[q]
              q1=q
              if q.startswith('##'):q1=q[2:]
              elif q.startswith('#'):q1=q[1:]
              choices['##compiler_flags#'+q1]=qq

    ###############################################################################################################
    # PIPELINE SECTION: get compiler vars choices (-Dvar=value) - often for datasets such as in polyhedral benchmarks
    bcvd=meta.get('build_compiler_vars_desc',{})
    cbcvd=choices.get('##compiler_vars',{})

    if len(bcvd)>0 and len(cbcvd)==0:
       for q in bcvd:
           qq=bcvd[q]
           q1=q
           if q.startswith('##'):q1=q[2:]
           elif q.startswith('#'):q1=q[1:]
           choices['##compiler_vars#'+q1]=qq

    cv=i.get('compiler_vars',{})

    ###############################################################################################################
    # PIPELINE SECTION: target platform features
    npf=i.get('no_platform_features','')
    if i.get('platform_features','')!='yes' and npf!='yes':
       if o=='con':
          ck.out(sep)
          ck.out('Detecting all target platform features ...')
          ck.out('')

       # Get some info about platforms
       ii={'action':'detect',
           'module_uoa':cfg['module_deps']['platform'],
           'host_os':hos,
           'target_os':tos,
           'device_id':tdid,
           'skip_print_os':'yes',
           'skip_device_init':sdi,
           'skip_info_collection':sic,
           'out':oo}
       r=ck.access(ii)
       if r['return']>0: return r

       features['platform']=r.get('features',{})
       i['platform_features']='yes'
       i['skip_info_collection']='yes'

    ###############################################################################################################
    # Pipeline ready for compile/run
    i['ready']='yes'
    if pr=='yes':
       return finalize_pipeline(i)

    ###############################################################################################################
    # PIPELINE SECTION: Compile program
    cs='yes'
    if i.get('no_compile','')!='yes':
       if o=='con':
          ck.out(sep)
          ck.out('Compile program ...')
          ck.out('')

       cl=i.get('clean','')
       if cl=='' and i.get('no_clean','')!='yes': cl='yes'

       if meta.get('no_compile','')!='yes':
          ii={'sub_action':'compile',
              'host_os':hos,
              'target_os':tos,
              'deviced_id':tdid,
              'path':pdir,
              'meta':meta,
              'deps':cdeps,
              'generate_rnd_tmp_dir':grtd,
              'tmp_dir':tdir,
              'clean':cl,
              'skip_clean_after':sca,
              'compile_type':ctype,
              'flags':flags,
              'lflags':lflags,
              'console':cons,
              'env':env,
              'extra_env':eenv,
              'compiler_vars':cv,
              'out':oo}
          r=process_in_dir(ii)
          if r['return']>0: return r

          misc=r['misc']
          tdir=misc.get('tmp_dir','')
          if tdir!='': i['tmp_dir']=tdir

          cch=r['characteristics']
          chars['compile']=cch

          xct=cch.get('compilation_time',-1)
          xos=cch.get('obj_size',-1)

          cs=misc.get('compilation_success','')
          if cs=='no': i['fail']='yes'

    ###############################################################################################################
    # PIPELINE SECTION: Run program
    if cs!='no' and i.get('no_run','')!='yes':
       if o=='con':
          ck.out(sep)
          ck.out('Running program ...')

       ii={'sub_action':'run',
           'host_os':hos,
           'target_os':tos,
           'deviced_id':tdid,
           'path':pdir,
           'console':cons,
           'meta':meta,
           'deps':cdeps,
           'cmd_key':kcmd,
           'dataset_uoa':dduoa,
           'generate_rnd_tmp_dir':grtd,
           'tmp_dir':tdir,
           'skip_clean_after':sca,
           'compile_type':ctype,
           'flags':flags,
           'lflags':lflags,
           'repeat':repeat,
           'skip_calibration':rsc,
           'calibration_time':rct,
           'calibration_max':rcm,
           'env':env,
           'extra_env':eenv,
           'compiler_vars':cv,
           'out':oo}
       r=process_in_dir(ii)
       if r['return']>0: return r

       misc=r['misc']
       tdir=misc.get('tmp_dir','')
       if tdir!='': i['tmp_dir']=tdir

       rch=r['characteristics']
       chars['run']=rch

       csuc=misc.get('calibration_success',True)
       rs=misc.get('run_success','')

       if rs=='no' or not csuc:
          i['fail']='yes'

    ###############################################################################################################
    # Deinit remote device, if needed
    ndi=i.get('no_deinit_remote_device','')
    if remote=='yes' and ndi!='yes':
       r=ck.access({'action':'init_device',
                    'module_uoa':cfg['module_deps']['platform'],
                    'os_dict':tosd,
                    'device_id':tdid,
                    'key':'remote_deinit'})
       if r['return']>0: return r

    ###############################################################################################################
    # PIPELINE SECTION: finalize PIPELINE
    return finalize_pipeline(i)

##############################################################################
# finalize pipeline
def finalize_pipeline(i):
    """
    Input:  {
              Input from pipeline that will be passed as output
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')

    tmp=i.get('tmp',{})
    pr=i.get('prepare','')

    fail=i.get('fail','')

    stfx=i.get('save_to_file','')
    stf=stfx
    cd=tmp.get('cur_dir','')
    if not os.path.isabs(stf):
       stf=os.path.join(cd, stf)

    # Cleaning input/output
    for q in cfg['clean_vars_in_output']:
        if q in i:
           del(i[q])

    if stfx!='':
       if o=='con':
          ck.out(sep)
          ck.out('Writing state to file '+stf+' ...')

       rx=ck.save_json_to_file({'json_file':stf,
                                'dict':i,
                                'sort_keys':'yes'})
       if rx['return']>0: return rx

    if o=='con':
       ck.out(sep)
       if i.get('ready','')=='yes':
          if pr=='yes':
             ck.out('Pipeline is ready!')
          else:
             if fail=='yes':
                ck.out('Pipeline failed!')
             else:
                ck.out('Pipeline executed successfully!')
       else:
          ck.out('Pipeline is NOT YET READY - multiple choices exists!')

    i['return']=0

    return i

##############################################################################
# select uoa

def select_uoa(i):
    """
    Input:  {
              choices - list from search function
            }

    Output: {
              return  - return code =  0, if successful
                                    >  0, if error
              (error) - error text if return > 0
              choice  - data UOA
            }

    """

    lst=i.get('choices',[])

    zz={}
    iz=0
    for z1 in sorted(lst, key=lambda v: v['data_uoa']):
        z=z1['data_uid']
        zu=z1['data_uoa']

        zs=str(iz)
        zz[zs]=z

        ck.out(zs+') '+zu+' ('+z+')')

        iz+=1

    ck.out('')
    rx=ck.inp({'text':'Choose first number to select UOA: '})
    x=rx['string'].strip()

    if x not in zz:
       return {'return':1, 'error':'number is not recognized'}

    dduoa=zz[x]

    return {'return':0, 'choice':dduoa}

##############################################################################
# select list

def select_list(i):
    """
    Input:  {
              choices - simple text list of choices
            }

    Output: {
              return  - return code =  0, if successful
                                    >  0, if error
              (error) - error text if return > 0
              choice  - selected text
            }

    """

    lst=i.get('choices',[])

    zz={}
    iz=0
    for z in lst:
        zs=str(iz)
        zz[zs]=z

        ck.out(zs+') '+z)

        iz+=1

    ck.out('')
    rx=ck.inp({'text':'Choose first number to select item: '})
    x=rx['string'].strip()

    if x not in zz:
       return {'return':1, 'error':'number is not recognized'}

    dduoa=zz[x]

    return {'return':0, 'choice':dduoa}
