#
# Collective Knowledge (pipeline)
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
# setup pipeline

def setup(i):
    """
    Input:  {
              data_uoa     - pipeline module UOA (such as 'benchmark')
                or
              pipeline_uoa
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    puoa=i.get('data_uoa','')
    if puoa=='':
       puoa=i.get('pipeline_uoa','')
    if puoa=='':
       return {'return':1, 'error':'pipeline_uoa is not defined'}

    r={'return':0}

    setup_completed=False
    while not setup_completed:
       ii={'action':'pipeline',
           'module_uoa':puoa,
           'prepare':'yes',
           'out':o}
       r=ck.access(ii)
       if r['return']>0: return r

       ready=r.get('ready','')
       if ready=='yes':
          setup_completed=True

    return r

##############################################################################
# universal pipeline autotuning

def autotune(i):
    """
    Input:  {
               (data_uoa)             - pipeline module UOA

               (pipeline)             - prepared pipeline setup (already ready to run)
                     or 
               (pipeline_from_file)   - load prepared pipeline setup from file

               (pipeline_update)      - update pipeline with this dict (useful to update already prepared pipeline from file)

               (iterations)           - limit number of iterations, otherwise infinite (default=50)
               (start_from_iteration) - skip all iterations before this number
               (repetitions)          - statistical repetitions (default=4)

               (seed)                 - if !='', use as random seed (to reproduce experiments)

               Enforce exploration:
               (start)
               (stop)
               (step)
               (explore_type)         = random, parallel-random, loop, parallel-loop, 
                                        machine-learning-based, model-based, adaptive, 
                                        plugin-based, customized

                    or
               (random)
               (parallel-random)
               (loop)
               (parallel-loop)
               (machine-learning-based)
               (model-based)
               (adaptive)
               (plugin-based)
               (customized)

               (record)               - (data UOA) explicitly record to this entry
               (record_repo)          - (repo UOA) explicitly select this repo to record
               (record_failed)        - if 'yes', record even failed experiments
                                        (for debugging, buildbots, detecting designed 
                                         architecture failures, etc)
               (record_ignore_update) - (default=yes), if 'yes', skip recording date/author info for each update


               (state)                - pre-load state preserved across iterations
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import fnmatch
    import json
    import random

    o=i.get('out','')

    ic=copy.deepcopy(i)
    ic['module_uoa']=''
    ic['action']=''
    ic['cid']=''
    ic['data_uoa']=''

    record=ic.get('record','')
    if 'record' in ic: del(ic['record'])
    record_repo=ic.get('record_repo','')
    if 'record_repo' in ic: del(ic['record_repo'])
    record_failed=ic.get('record_failed','')
    if 'record_failed' in ic: del(ic['record_failed'])
    record_ignore_update=ic.get('record_ignore_update','')
    if record_ignore_update=='': record_ignore_update='yes'
    if 'record_ignore_update' in ic: del(ic['record_ignore_update'])

    state=i.get('state',{})

    jtype=i.get('explore_type','')
    if i.get('random','')=='yes': jtype='random'
    elif i.get('loop','')=='yes': jtype='loop'
    elif i.get('parallel-loop','')=='yes': jtype='parallel-loop'
    elif i.get('parallel-random','')=='yes': jtype='parallel-random'
    elif i.get('machine-learning-based','')=='yes' or \
         i.get('model-based','')=='yes' or \
         i.get('adaptive','')=='yes' or \
         i.get('plugin-based','')=='yes' or \
         i.get('customized','')=='yes': jtype='customized' 
    cexp={'type':jtype, 
          'omit_probability':i.get('omit_probability',''),
          'start':i.get('start',''),
          'stop':i.get('stop',''),
          'step':i.get('step','')}

    # Check data_uoa
    puoa=i.get('data_uoa','')
    if puoa=='':
       return {'return':1, 'error':'data_uoa is not set, i.e. no pipeline module'}

    # Check that data_uoa is module that exists
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['module'],
                 'data_uoa':puoa})
    if r['return']>0: return r
    d=r['dict']
    if d.get('pipeline','')!='yes':
       return {'return':1, 'error':'selected pipeline module is not pipeline'}

    # Check meta
    pipeline=i.get('pipeline',{})

    pff=i.get('pipeline_from_file','')
    if pff!='':
       r=ck.load_json_file({'json_file':pff})
       if r['return']>0: return r
       pipeline=r['dict']

    pipeline_update=i.get('pipeline_update',{})
    if len(pipeline_update)!=0:
       r=ck.merge_dicts({'dict1':pipeline, 'dict2':pipeline_update})
       if r['return']>0: return r
       pipeline=r['dict1']

    # If pipeline meta is not defined, set up pipeline ...
    if len(pipeline)==0:
       ii=copy.deepcopy(ic)
       ii['module_uoa']=puoa
       ii['action']='pipeline'
       ii['prepare']='yes'
       pipeline=ck.access(ii)
       if pipeline['return']>0: return pipeline
       if pipeline.get('fail','')=='yes':
          return {'return':1, 'error':'pipeline setup failed'}
       if pipeline.get('ready','')!='yes':
          return {'return':1, 'error':'pipeline is not ready'}
       del(pipeline['return'])
       
    # Copy pipeline
    pipeline['prepare']='no'
    pipeline['module_uoa']=puoa
    pipeline['action']='pipeline'
    pipeline['out']=o
    pipelinec=copy.deepcopy(pipeline)
          
    # Check some vars ...
    ni=i.get('iterations','')
    if ni=='': ni=50
    try: ni=int(ni)
    except Exception as e: pass

    sfi=i.get('start_from_iteration','')
    if sfi=='': sfi=1
    if type(sfi)!=int: sfi=int(sfi)
   
    srm=i.get('repetitions','')
    if srm=='': srm=4
    try: srm=int(srm)
    except Exception as e: pass

    # Check choices descriptions and dimensions
    cdesc=pipeline.get('choices_desc',{})
    cdims=i.get('choices_dims',[])
    csel=i.get('choices_selection',{})
    ccur=[]

    # Prepare multi-dimensional vector of choices
    dv1=[] # Current dimensions
    for iq1 in range(0,len(cdims)):
        q1=cdims[iq1]
        dv=[]
        zz=csel[iq1]
        ztags=zz.get('tags','').split(',')
        znotags=zz.get('notags','').split(',')
        for q2 in q1:
            if '*' in q2 or '?' in q2:
               for k in sorted(cdesc, key=lambda v: cdesc[v].get('sort',0)):
                   if fnmatch.fnmatch(k,q2):
                      # Check tags
                      yy=cdesc[k].get('tags',[])
                      add=True
                      for j in ztags:
                          j=j.strip()
                          if j!='' and j not in yy:
                             add=False
                             break
                      if add:
                         for j in znotags:
                             j=j.strip()
                             if j!='' and j in yy:
                                add=False
                                break
                         if add:
                            dv.append(k)   
            else:
               dv.append(q2)   
        dv1.append(dv)
    cdims=dv1

    # Check seed
    seed=i.get('seed','')
    if seed!='':
       random.seed(int(seed))

       if o=='con':
          ck.out('')
          ck.out('Random seed: '+str(seed))
          ck.out('')

    # Start iterations
    finish=False
    for m in range(0,ni):
        mm=m+1
        ck.out(sep)
        ck.out('Pipeline iteration: '+str(mm)+' of '+str(ni))

        # Copy original
        if m==0 or mm>=sfi:
           pipeline=copy.deepcopy(pipelinec)

        # Make selection
        r=ck.access({'module_uoa':cfg['module_deps']['choice'],
                     'action':'make',
                     'choices_desc':cdesc,
                     'choices_dims':cdims,
                     'choices_selection':csel,
                     'choices_current':ccur,
                     'custom_explore':cexp,
                     'pipeline':pipeline,
                     'out':o})
        if r['return']>0: return r

        if r['finish']:
           finish=True
           break

        # Check if pass this iteration
        if mm<sfi:
           ck.out('')
           ck.out('  (skiped by request)')
           continue

        # Describing experiment
        dd={'features':pipeline.get('features',{})}
        ddcl=[] # characteristics list

        for sr in range(0, srm):
            ck.out('')
            ck.out('      ------------------- Statistical reptition: '+str(sr+1)+' of '+str(srm)+' -------------------')
            ck.out('')

            pipeline1=copy.deepcopy(pipeline)
            pipeline1['out']=o
            pipeline1['state']=state
            pipeline1['statistical_repetition_number']=sr
            rx=ck.access(pipeline1)
            if rx['return']>0: return rx

            state=rx.get('state',{})

            fail=rx.get('fail','')

            if fail!='yes' or record_failed=='yes':
               ddcl.append(pipeline1.get('characteristics',{}))
            dd['characteristics_list']=ddcl

            if fail=='yes': break

        if record!='':
           if fail!='yes' or record_failed=='yes':
               ##########################################################################################
               # Recording experiment
               if o=='con':
                  ck.out(sep)
                  ck.out('Recording experiment ...')
                  ck.out('')

#               raw_input('recording ...')

               ie={'action':'add',

                   'module_uoa':cfg['module_deps']['experiment'],

                   'ignore_update':record_ignore_update,
                   'out':'con',
                   'sort_keys':'yes',

                   'experiment_repo_uoa': record_repo,
                   'experiment_uoa':record,

#                   'search_point_by_features':'yes',
#                   'process_multi_keys':['characteristics','features'],
                   'record_all_subpoints':'yes',

#                   'force_new_entry':'yes',

                   'dict':dd}

               rx=ck.access(ie)
               if rx['return']>0: return rx

    if finish:
       ck.out('')
       ck.out('All iterations are done!')

    if m>0:
       ck.out(sep)
       ck.out('Autotuning finished!')

    return {'return':0}

##############################################################################
# Run pipeline once ...

def run(i):
    """
    Input:  {
              (iterations) - default =1
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    if i.get('iterations','')=='': i['iterations']=1
    return autotune(i)
