#
# Collective Knowledge (Check speedup of program versus various compiler flags and data sets)
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
sep='**********************************************************************'

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
# describe experiment

def describe(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    ck.out(cfg['full_desc'])

    return {'return':0}

##############################################################################
# reproduce experiment

def reproduce(i):
    """
    Input:  {
              program_uoa      - program UOA to check

              (cmd_key)        - cmd key
              (dataset_uoas)   - check dataset UOA

              (choices)        - dict['flags'] - list of combinations of compiler flags

              (host_os)        - host OS (detect, if omitted)
              (target_os)      - OS module to check (if omitted, analyze host)
              (device_id)      - device id if remote (such as adb)






            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    puoa=i.get('program_uoa','')
    if puoa=='':
       return {'return':1, 'error':'program_uoa is not defined.\n\nUse "ck list program" to see available programs.\nUse "ck pull repo:ck-programs" and "ck pull repo:ck-datasets-min" to get a small set of our benchmarks and datasets.'}

    choices=i.get('choices',{})
    if len(choices)==0:
       choices=cfg['choices']

    cflags=choices.get('flags',[])
    if len(cflags)==0:
       return {'return':1, 'error':'choices dictionary doesn\'t have "flags" list'}

    ###################################################
    # Experiment table
    table=[]

    ###################################################
    ck.out(sep)
    ck.out('Loading program meta info ...')
    
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':puoa})
    if r['return']>0: return r
    pd=r['dict']

    cmd_key=i.get('cmd_key','')
    if cmd_key=='': cmd_key='default'

    ###################################################
    ck.out(sep)
    ck.out('Checking available data sets ...')

    dsets=i.get('dataset_uoas',[])

    dtags=pd.get('run_cmds',{}).get(cmd_key,{}).get('dataset_tags','')

    ii={'action':'search',
        'module_uoa':cfg['module_deps']['dataset']}
    if len(dsets)>0:
       ii['data_uoa_list']=dsets
    else:
       ii['tags']=dtags
    r=ck.access(ii)
    if r['return']>0: return r
    dlist=r['lst']

    # Prepare first and second line of table
    t=[]
    t.append('')
    t.append('')
    t.append('')
    for ds in dlist:
        t.append('Dataset '+ds['data_uoa']+':')
    table.append(t)

    t=[]
    t.append('Optimization:')
    t.append('Binary size:')
    t.append('MD5SUM:')
    for ds in dlist:
        t.append('min time - max time:')
    table.append(t)


    t=[]
    t.append('-O3')
    t.append('123')
    t.append('3432')
    for ds in dlist:
        t.append('5.343 - 5.555')
    table.append(t)

    # Draw table
    ii={'action':'draw',
        'module_uoa':cfg['module_deps']['table'],
        'table':table,
        'out':'txt'}
    r=ck.access(ii)
    if r['return']>0: return r
    s=r['string']



    ii['out']='html'
    r=ck.access(ii)
    if r['return']>0: return r
    html=r['string']
        
    print html



    return {'return':0}
