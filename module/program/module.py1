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
       else:
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
           ck.out('********************************************************************************')

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
# compile program

def process_in_dir(i):
    """
    Input:  {
              The same as 'compile'

              sub_action   - clean, compile, run

              path         - path
              meta         - program description

              (repo_uoa)   - program repo UOA
              (module_uoa) - program module UOA
              (data_uoa)   - program data UOA
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    import os

    o=i.get('out','')

    rx=ck.get_platform({})
    if rx['return']>0: return rx
    ios=rx['platform']

    p=i['path']
    meta=i['meta']

    ruoa=i.get('repo_uoa', '')
    muoa=i.get('module_uoa', '')
    duoa=i.get('data_uoa', '')

    # If muoa=='' assume program
    if muoa=='':
       muoa=work['self_module_uid']

    if duoa=='':
       x=meta.get('backup_data_uid','')
       if x!='':
          duoa=meta['backup_data_uid']

    ########## Check common vars ################
    # Check if use obj ext
    obj_ext=''
    xobj_ext=meta.get('obj_extension',{})
    if len(xobj_ext)>0:
       obj_ext=xobj_ext.get(ios,'')
       if obj_ext=='':
          obj_ext=xobj_ext.get('all','')

    # Check if use bin
    bin_file=''
    xbin_file=meta.get('bin_file',{})
    if len(xbin_file)>0:
       bin_file=xbin_file.get(ios,'')
       if bin_file=='':
          bin_file=xbin_file.get('all','')

    # Check if compile in tmp dir
    cdir=p

    x=i.get('process_in_tmp','').lower()
    if x=='': x='yes'
    if x!='yes':
       x=meta.get('process_in_tmp','').lower()
    if x=='yes':
       td=i.get('tmp_dir','')
       if td=='': td='tmp'

       if i.get('generate_rnd_tmp_dir','')=='yes':
          # Generate tmp dir
          import tempfile
          fd, fn=tempfile.mkstemp(suffix='', prefix='tmp-ck-')
          os.close(fd)
          os.remove(fn)

          cdir=os.path.join(p, fn)
          print cdir
       else:
          cdir=td

    if cdir!='' and not os.path.isdir(cdir):
       os.mkdir(cdir)

    os.chdir(cdir)
    rcdir=os.getcwd()

    sa=i['sub_action']

    # Check sub_actions
    ################################### Compile ######################################
    if sa=='compile':
       sfs=meta.get('source_files',[])

       # Check if compile individual files
       xcif=meta.get('compile_individual_files_cmd',{})
       obj_files=[]

       if len(xcif)>0:
          if len(sfs)==0:
             return {'return':1, 'error':'can\'t compile individual files since source files are not specified in description'}

          cif=xcif.get(ios,'')
          if cif=='':
             cif=xcif.get('all','')
          if cif=='':
             return {'return':1, 'error':'can\'t find compile CMD for the platform'}

          for sf in sfs:
              cif1=cif
              sf0=os.path.splitext(sf)[0]

              psf=os.path.join(p, sf)
              psf0=os.path.splitext(psf)[0]

              cif1=cif1.replace('$#COMPILER#$', 'cl')
              cif1=cif1.replace('$#COMPILER_FLAGS_BEFORE#$', '/c ')
              cif1=cif1.replace('$#COMPILER_FLAGS_AFTER#$', '')

              cif1=cif1.replace('$#SOURCE_FILE#$', psf)

              if obj_ext!='':
                 cif1=cif1.replace('$#OBJ_FILE#$', sf0)
                 cif1=cif1.replace('$#OBJ_EXT#$', obj_ext)
                 cif1=cif1.replace('$#COMPILER_OBJ_FLAG#$', '/Fo')
              else:
                 cif1=cif1.replace('$#COMPILER_OBJ_FLAG#$$#OBJ_FILE#$$#OBJ_EXT#$','')

              if o=='con':
                 ck.out('    '+cif1)
              rx=os.system(cif1)
              if rx>0:
                 return {'return':1, 'error': 'compilation failed'}

       else:
          print 'checking if build script'










       # Check if link individual files
       ycif=meta.get('link_individual_files_cmd',{})
       if len(ycif)>0:
          if len(sfs)==0:
             return {'return':1, 'error':'can\'t link individual files since source files are not specified in description'}

          cif=ycif.get(ios,'')
          if cif=='':
             cif=ycif.get('all','')
          if cif=='':
             return {'return':1, 'error':'can\'t find link CMD for the platform'}

          obj_files=''
          for sf in sfs:
              cif1=cif
              sf0=os.path.splitext(sf)[0]
              psf=os.path.join(p, sf)
              psf0=os.path.splitext(psf)[0]

              if obj_files!='': obj_files+=' '
              obj_files+=sf0+obj_ext

          cif1=cif1.replace('$#LINKER#$', 'link')
          cif1=cif1.replace('$#LINKER_FLAGS_BEFORE#$', '')
          cif1=cif1.replace('$#LINKER_FLAGS_AFTER#$', '/out:'+bin_file)

          cif1=cif1.replace('$#OBJ_FILES#$', obj_files)
              
          if o=='con':
             ck.out('    '+cif1)
          rx=os.system(cif1)
          if rx>0:
             return {'return':1, 'error': 'compilation failed'}

       else:
          print 'checking if build script'

    ################################### Clean ######################################
    elif sa=='clean':
       print 'tbd'


    ################################### Run ######################################
    elif sa=='run':
       run_cmds=meta.get('run_cmds',{})
       if len(run_cmds)==0:
          return {'return':1, 'error':'no CMD for run'}

       krun_cmds=sorted(list(run_cmds.keys()))

       cmd=i.get('cmd_key','')
       if cmd=='':
          if 'default' in krun_cmds: cmd='default'
          else: cmd=krun_cmds[0]
       else:
          if cmd not in krun_cmds:
             return {'return':1, 'error':'CMD key not found in program description'}

       vcmd=run_cmds[cmd]

       c=''

       rt=vcmd.get('run_time',{})

       c=rt.get('run_cmd_main','')
       if c=='':
          return {'return':1, 'error':'cmd is not defined'}

       # Replace bin file
       c=c.replace('$#BIN_FILE#$', bin_file)
       c=c.replace('$#os_dir_separator#$', os.sep)

       # Check if takes datasets from CK
       dtags=vcmd.get('dataset_tags',[])
       if len(dtags)>0:
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

             dduoa=lst[0].get('data_uid','')

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
             df0=dfiles[0]
             c=c.replace('$#dataset_filename#$', df0)

       print c
       if o=='con':
          ck.out('    '+c)
       rx=os.system(c)
       if rx>0 and vcmd.get('ignore_return_code','').lower()!='yes':
          return {'return':1, 'error': 'execution failed'}

    return {'return':0, 'tmp_dir':rcdir}

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
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    print ('auto-tuning program')

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

    print ('crowdtuning program')

    return {'return':0}
