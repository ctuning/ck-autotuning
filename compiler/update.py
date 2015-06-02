import ck.kernel as ck

r=ck.access('list compiler:* out=none')
if r['return']>0: 
   print 'Error: '+r['error']
   exit(1)

for q in r['lst']:
    m=q['module_uoa']
    d=q['data_uoa']
    ruoa=q['repo_uoa']

    print d

    r=ck.access({'action':'load',
                 'module_uoa':m,
                 'data_uoa':d})
    if r['return']>0: 
       print 'Error: '+r['error']
       exit(1)

    dd=r['dict']
    dm=r['info']
    dx=r.get('desc',{})

    zz=dd.get('all_compiler_flags_desc',{})
    if len(zz)>0:
       dx['all_compiler_flags_desc']=zz
    if 'all_compiler_flags_desc' in dd: del(dd['all_compiler_flags_desc'])

    rvd=dd.get('run_vars_desc',{})
    if len(rvd)>0:
       dx['run_vars_desc']=rvd
    if 'run_vars_desc' in dd: del(dd['run_vars_desc'])

    rx=ck.access({'action':'update',
                  'repo_uoa':ruoa,
                  'module_uoa':m,
                  'data_uoa':d,
                  'dict':dd,
                  'desc':dx,
                  'substitute':'yes',
                  'ignore_update':'yes',
                  'sort_keys':'yes'})
    if rx['return']>0:
       print 'Error: '+rx['error']
       exit(1)
