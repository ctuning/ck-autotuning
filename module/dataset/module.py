#
# Collective Knowledge (dataset)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
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
# Import all files to meta

def import_all_files(i):
    """
    Input:  {
               data_uoa
               (repo_uoa)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    duoa=i['data_uoa']
    ruoa=i.get('repo_uoa','')

    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa,
                 'repo_uoa':ruoa})
    if r['return']>0: return r

    duid=r['data_uid']
    d=r['dict']
    p=r['path']

    if 'dataset_files' not in d: d['dataset_files']=[]
    dfiles=d['dataset_files']

    dirList=os.listdir(p)
    for fn in dirList:
         p1=os.path.join(p, fn)
         if os.path.isfile(p1):
            if fn not in dfiles:
               dfiles.append(fn)

    r=ck.access({'action':'update',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duid,
                 'repo_uoa':ruoa,
                 'dict':d,
                 'substitute':'yes',
                 'sort_keys':'yes'})
    if r['return']>0: return r

    return {'return':0}

##############################################################################
# TBD: generate new data sets to cover unseen behavior
# See https://scholar.google.com/citations?view_op=view_citation&citation_for_view=IwcnpkwAAAAJ:hqOjcs7Dif8C
#     http://arxiv.org/abs/1506.06256

def generate(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    print ('TBD: generate new data sets to cover unseen behavior')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}

##############################################################################
# TBD: prune data sets to find minimal representative data set covering behavior
# See https://scholar.google.com/citations?view_op=view_citation&citation_for_view=IwcnpkwAAAAJ:hqOjcs7Dif8C
#     http://arxiv.org/abs/1506.06256

def prune(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    print ('prune data sets to find minimal representative data set covering behavior')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}
