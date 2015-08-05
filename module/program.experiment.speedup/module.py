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

              (stat_repeat)    - max statistical repetitions (4 by default)

              (check_speedup)  - if 'yes', check speedups for the first two optimizations ...
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
    table=[]  # Strings (for printing)
    otable=[] # Original format

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
        t.append('min time (s); exp time (s); var (%):')
    table.append(t)

    # Number of statistical repetitions
    srepeat=int(i.get('stat_repeat',0))
    if srepeat<1: srepeat=4

    repeat=i.get('repeat',-1)
    
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')

    # will be updated later
    deps={}
    features={}

    dcomp=''

    for cf in cflags:
        ck.out(sep)
        ck.out('Checking flags "'+cf+'" ...')

        t=[]
        t.append(cf)

        ii={'action':'run',

            'module_uoa':cfg['module_deps']['pipeline'],
            'data_uoa':cfg['module_deps']['program'],
            'program_uoa':puoa,

            'host_os':hos,
            'target_os':tos,
            'device_id':tdid,

            'flags':cf,

            'repetitions': 1,

            'no_run':'yes',

            'out':'con'}

        if len(deps)>0: ii['dependencies']=deps

        r=ck.access(ii)
        if r['return']>0: return r
            
        lio=r.get('last_iteration_output',{})

        fail=lio.get('fail','')

        if fail=='yes':
           return {'return':1, 'error':'compilation failed ('+lio.get('fail_reason','')+')- check above output and possibly report to the authors!'}

        ed=r.get('experiment_desc',{})
        deps=ed.get('dependencies',{})
        
        cc=ed.get('choices',{})

        hos=cc['host_os']
        tos=cc['target_os']
        tdid=cc['device_id']

        ft=ed.get('features',{})
        if len(features)==0: features=ft

        if dcomp=='': dcomp=ft.get('compiler_version',{}).get('str','')

        lsa=r.get('last_stat_analysis',{})
        fresults=lsa.get('dict_flat',{})

        os=fresults.get('##characteristics#compile#obj_size#min',0)
        md5=fresults.get('##characteristics#compile#obj_size#md5_sum','')

        t.append(os)
        t.append(md5)

        # Iterate over datasets
        oresults={}

        for ds in dlist:
            duoa=ds['data_uoa']
            duid=ds['data_uid']

            ck.out(sep)
            ck.out('Running with dataset '+duoa+' ...')
            ck.out('')

            ij={'action':'run',

                'module_uoa':cfg['module_deps']['pipeline'],
                'data_uoa':cfg['module_deps']['program'],
                'program_uoa':puoa,

                'host_os':hos,
                'target_os':tos,
                'device_id':tdid,

                'repetitions': srepeat,

                'cmd_key':cmd_key,
                'dataset_uoa':duid,
                'no_compile':'yes',

                'out':'con'}

            if repeat>0: ij['repeat']=repeat

            r=ck.access(ij)
            if r['return']>0: return r

            lio=r.get('last_iteration_output',{})

            fail=lio.get('fail','')

            if fail=='yes':
               return {'return':1, 'error':'execution failed ('+lio.get('fail_reason','')+')- check above output and possibly report to the authors!'}

            state=lio.get('state',{})
            repeat=state['repeat']

            lsa=r.get('last_stat_analysis',{})
            fresults=lsa.get('dict_flat',{})

            texp=fresults.get('##characteristics#run#execution_time_kernel_0#exp',0)
            tmin=fresults.get('##characteristics#run#execution_time_kernel_0#min',0)
            tdelta=fresults.get('##characteristics#run#execution_time_kernel_0#range_percent',0)

            oresults[duoa]=fresults

            t.append('      '+('%3.3f' % tmin) + ' ;       ' + ('%3.3f' % texp) + ' ;   ' + ('%4.1f' % (tdelta*100))+'%')

        otable.append(oresults)
        table.append(t)

    # Draw table
    ii={'action':'draw',
        'module_uoa':cfg['module_deps']['table'],
        'table':table,
        'out':'txt'}
    r=ck.access(ii)
    if r['return']>0: return r
    s=r['string']

    rf=cfg['report_file']
    rft=rf+'.txt'
    rfh=rf+'.html'
    rfj=rf+'.json'

    ck.out(sep)
    ck.out('Raw results (exported to '+rf+'.txt, .html, .json):')
    
    if dcomp!='':
       ck.out('')
       ck.out('Detected compiler version: '+dcomp)
     
    ck.out('')
    ck.out(s)

    r=ck.save_text_file({'text_file':rft, 'string':s})
    if r['return']>0: return r

    ii['out']='html'
    r=ck.access(ii)
    if r['return']>0: return r
    html=r['string']

    r=ck.save_text_file({'text_file':rfh, 'string':html})
    if r['return']>0: return r

    # Checking if there is a speedup ...
    # Expect that otable[0] - -O3; otable[1] - -O3 -fno-if-conversion
    if i.get('check_speedup','')=='yes' and len(otable)>1:
       r0d0=otable[0][dlist[0]['data_uoa']]
       r0d1=otable[0][dlist[1]['data_uoa']]
       r1d0=otable[1][dlist[0]['data_uoa']]
       r1d1=otable[1][dlist[1]['data_uoa']]

       t0d0=r0d0['##characteristics#run#execution_time_kernel_0#exp']
       t0d1=r0d1['##characteristics#run#execution_time_kernel_0#exp']
       t1d0=r1d0['##characteristics#run#execution_time_kernel_0#exp']
       t1d1=r1d1['##characteristics#run#execution_time_kernel_0#exp']

       sd0=t0d0/t1d0
       sd1=t0d1/t1d1

       if sd0>1.1 or sd1>1.1 or sd0<0.9 or sd1<0.9:
          ck.out(sep)
          ck.out('Found speedup or slow down for the first 2 optimizations:')
          ck.out('')
          ck.out(' Dataset 0 ('+dlist[0]['data_uoa']+') speedup (T_opt0/T_opt1) = '+('%2.2f' % sd0))
          ck.out(' Dataset 1 ('+dlist[1]['data_uoa']+') speedup (T_opt0/T_opt1) = '+('%2.2f' % sd1))

    return {'return':0}
