#
# Collective Knowledge (benchmark pipeline (workflow))
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
# run benchmark

def run(i):
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

    print i
    exit(1)



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

    return {'return':0}
