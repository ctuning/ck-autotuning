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

               (process_multi_keys)   - list of keys (starts with) to perform stat analysis on flat array,
                                           by default ['##characteristics#*', '##features#*' '##choices#*'],
                                           if empty, no stat analysis

               (record)               - if 'yes', record results
               (record_uoa)           - (data UOA or CID where module_uoa ignored!) explicitly record to this entry
               (record_repo)          - (repo UOA) explicitly select this repo to record
               (record_failed)        - if 'yes', record even failed experiments
                                        (for debugging, buildbots, detecting designed 
                                         architecture failures, etc)
               (record_ignore_update) - (default=yes), if 'yes', skip recording date/author info for each update
               (tags)                 - record these tags to the entry description
               (subtags)              - record these subtags to the point description

               (record_params)        - extra record parameters (to 'add experiment' function)

               (features_keys_to_process)    - list of keys for features (and choices) to process/search 
                                                    when recording experimental results (can be wildcards)
                                                    by default ['##features#*', '##choices#*', '##choices_order#*']

               (frontier_keys)        - list of keys to leave only best points during multi-objective autotuning
                                        (multi-objective optimization)

               (frontier_features_keys_to_ignore) - list of keys to ignore from 'features_keys_to_process' 
                                                    when detecting subset of points to detect frontier
                                                    (usually removing optimization dimensions, such as compiler flags)

               (features)             - extra features
               (meta)                 - extra meta

               (state)                - pre-load state preserved across iterations

               (save_to_file)         - if !='', save output dictionary to this file
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              last_iteration_output - output of last iteration
              last_stat_analysis    - flat dict with stat analysis
              experiment_desc       - dict with experiment description
            }

    """

    import copy
    import fnmatch
    import json
    from random import Random

    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    ic=copy.deepcopy(i)
    ic['module_uoa']=''
    ic['action']=''
    ic['cid']=''
    ic['data_uoa']=''

    tags=ck.get_from_dicts(ic, 'tags', [], None)
    tags=ck.convert_str_tags_to_list(tags) # if string, convert to list
    subtags=ck.get_from_dicts(ic, 'subtags', [], None)
    subtags=ck.convert_str_tags_to_list(subtags) # if string, convert to list

    stf=ck.get_from_dicts(ic, 'save_to_file', '', None)

    meta=ck.get_from_dicts(ic, 'meta', {}, None)

    pmk=ck.get_from_dicts(ic, 'process_multi_keys', '', None) # important, default should be '' to be processed later correctly ...

    fk=ck.get_from_dicts(ic, 'frontier_keys', [], None)

    record=ck.get_from_dicts(ic, 'record', '', None)
    record_uoa=ck.get_from_dicts(ic, 'record_uoa', '', None)
    record_repo=ck.get_from_dicts(ic, 'record_repo', '', None)
    if record.find(':')>=0:
       rx=ck.parse_cid({'cid':record})
       if rx['return']>0: return rx
       record=rx['data_uoa']
       record_repo=rx.get('repo_uoa','')
    record_failed=ck.get_from_dicts(ic, 'record_failed','', None)
    record_ignore_update=ic.get('record_ignore_update','')
    if record_ignore_update=='': record_ignore_update='yes'
    if 'record_ignore_update' in ic: del(ic['record_ignore_update'])

    rdict=ck.get_from_dicts(ic, 'record_params', {}, None)
    fkp=ck.get_from_dicts(ic, 'features_keys_to_process', [], None)
    ffki=ck.get_from_dicts(ic, 'frontier_features_keys_to_ignore', [], None)

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
    puid=''
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
    puid=r['data_uid']

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
       
    # Clean and copy pipeline before choice selection
    for q in cfg['clean_pipeline']:
        if q in pipeline: del(pipeline[q])
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
    corder=i.get('choices_order',[])
    csel=i.get('choices_selection',{})
    ccur=[]

    # most likely just one iteration - then set defaults
    if len(corder)==1 and len(csel)==0:
       csel=[{"type":"random"}]

    # Prepare multi-dimensional vector of choices
    dv1=[] # Current dimensions
    for iq1 in range(0,len(corder)):
        dv=[]
        q1=corder[iq1]
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
    corder=dv1

    # Check seed
    seed=i.get('seed','')
    if seed=='':
       my_random=Random()
    else:
       my_random=Random(int(seed))

       if o=='con':
          ck.out('')
          ck.out('Random seed: '+str(seed))
          ck.out('')

    # Keep best points if finding best points (possibly with Pareto)
    points={}

    # Start iterations
    rr={'return':0}
    stat_dict={'return':0}
    rrr={'return':0}
    dd={}
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
                     'choices_order':corder,
                     'choices_selection':csel,
                     'choices_current':ccur,
                     'custom_explore':cexp,
                     'pipeline':pipeline,
                     'random_module':my_random,
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
        dd={'tags':tags,
            'subtags':subtags,
            'meta':meta,
            'pipeline':pipelinec,
            'pipeline_uoa':puoa,
            'pipeline_uid':puid}

        ddcl=[] # characteristics list (from statistical repetitions)
        for sr in range(0, srm):
            ck.out('')
            ck.out('      ------------------- Statistical reptition: '+str(sr+1)+' of '+str(srm)+' -------------------')
            ck.out('')

            pipeline1=copy.deepcopy(pipeline)
            pipeline1['prepare']='no'
            pipeline1['module_uoa']=puoa
            pipeline1['action']='pipeline'
            pipeline1['out']=o
            pipeline1['state']=state
            pipeline1['autotuning_iteration']=m
            pipeline1['statistical_repetition_number']=sr
            rr=ck.access(pipeline1)
            if rr['return']>0: return rr

            state=rr.get('state',{})

            fail=rr.get('fail','')
            if fail!='yes' or record_failed=='yes':
               ddcl.append(pipeline1.get('characteristics',{}))

               if sr==0: # record for the first iteration otherwise pipeline may change via state ...
                  dd['choices']=rr.get('choices',{})
                  dd['choices_order']=rr.get('choices_order',[])
                  dd['choices_desc']=rr.get('choices_desc',{})
                  dd['features']=rr.get('features',{})
                  dd['features_desc']=rr.get('features_desc',{})
                  dd['dependencies']=rr.get('dependencies',{})
                  dd['characteristics_desc']=rr.get('characteristics_desc',{})

                  # TBD: CHECK HOW TO WRITE META HERE DEPENDING ON SCENARIOS ...

                  meta1=rr.get('meta',{})
                  if len(meta1)>0: meta.update(meta1)
                  dd['meta']=meta1

            if fail=='yes': break

        dd['characteristics_list']=ddcl

        ##########################################################################################
        # Recording experiment if needed
        stat_dict={}
        if record=='yes':

           # Will be reused for frontier
           iec={'module_uoa':cfg['module_deps']['experiment'],

                'experiment_repo_uoa': record_repo,
                'experiment_uoa':record_uoa,

                'features_keys_to_process':fkp}

           fft={} # flat features

           if fail!='yes' or record_failed=='yes':

              if o=='con':
                 ck.out(sep)
                 ck.out('Recording experiment ...')
                 ck.out('')

              ie=copy.deepcopy(iec)

              ie['action']='add'
              ie['ignore_update']=record_ignore_update
              ie['out']='con'
              ie['sort_keys']='yes'
              ie['record_all_subpoints']='yes'
              ie['process_multi_keys']=pmk
              ie['dict']=dd

              # Update what we record and how we process data from external dict -> 
              #  may be customized depending on scenarios 
              #  (compiler flag tuning, OpenCL/MPI params, etc)
              ie.update(rdict)

              rx=ck.access(ie)
              if rx['return']>0: return rx

              stat_dict=rx['dict_flat']
              rrr=rx['stat_analysis']
              fft=rx['flat_features']

        ##########################################################################################
        # If was not performed via recording, prform statistical analysis  here
        if fail!='yes' and len(stat_dict)==0:
           ii={'action':'multi_stat_analysis',
               'module_uoa':cfg['module_deps']['experiment'],
               'dict':stat_dict,
               'dict_to_add':dd,
               'process_multi_keys':pmk}
           rrr=ck.access(ii)
           if rrr['return']>0: return rrr
           stat_dict=rrr['dict_flat']

        # Check if need to leave only points on frontier 
        #   (our frontier is not 'Pareto efficient' since we have discreet characteristics)
        if len(fk)>0 and len(stat_dict)>0:
           # If data was recorded to repo, reload all points 
           if record=='yes':
              if o=='con':
                 ck.out('')
                 ck.out('  Reloading points to detect frontier ...')

              ie=copy.deepcopy(iec)

              ie['action']='get'
              ie['flat_features']=fft
              ie['features_keys_to_ignore']=ffki # Ignore parts of fetures to be able to create subset for frontier ...
              ie['skip_processing']='yes'
              ie['load_json_files']=['flat']
              ie['get_keys_from_json_files']=fk
              ie['out']='con'

              rx=ck.access(ie)
              if rx['return']>0: return rx

              xpoints=rx['points']
              ypoints={}
              points={}

              ip=0
              for q in xpoints:
                  rx=ck.gen_uid({})
                  if rx['return']>0: return rx
                  uid=rx['data_uid']

                  points[uid]=q.get('flat',{})
                  ypoints[uid]=ip
                  ip+=1
           else:
              rx=ck.gen_uid({})
              if rx['return']>0: return rx
              uid=rx['data_uid']

              w={}
              for q in stat_dict: 
                  if q in fk: w[q]=stat_dict[q]

              points[uid]=w

           # Filtering ...
           if o=='con':
              ck.out(sep)
              ck.out('Filtering multiple characteristics on Pareto frontier for multi-objective autotuning')
              ck.out('')

           # Save originals to know which ones to delete if recording ...
           rx=ck.access({'action':'filter',
                         'module_uoa':cfg['module_deps']['math.frontier'],
                         'points':points,
                         'out':oo})
           if rx['return']>0: return rx

           points=rx['points']
           dpoints=rx['deleted_points']

           # Delete filtered if record
           if record=='yes':
              # Clean original points
              ddpoints=[]
              for q in dpoints:
                  ip=ypoints[q]
                  ddpoints.append(xpoints[ip])

              # Attempt to delete points
              rx=ck.access({'action':'delete_points',
                            'module_uoa':cfg['module_deps']['experiment'],
                            'points':ddpoints,
                            'out':oo})
              if rx['return']>0: return rx

    # Mention, if all iterations were performed, or autotuning rached max number of iterations
    if finish:
       ck.out('')
       ck.out('All iterations are done!')

    if m>0:
       ck.out(sep)
       ck.out('Autotuning finished!')

    rz={'return':0, 'last_iteration_output':rr, 'last_stat_analysis': rrr, 'experiment_desc':dd}

    if stf!='':
       rx=ck.save_json_to_file({'json_file':stf, 'dict':rz, 'sort_keys':'yes'})

    return rz

##############################################################################
# Run pipeline once ...

def run(i):
    """
    Input:  {
              See 'autotune' with iterations=1 (to reuse statistical analysis and recoring to repo)

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
