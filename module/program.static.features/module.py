#
# Collective Knowledge (program - features)
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
# extract program static milepost features

def extract(i):
    """
    Input:  {
              (repo_uoa)        - repository UOA
              (data_uoa)        - program UOA (can be wildcards)

              (tags)            - tags to process specific programs

              (target_repo_uoa) - repo, where to save features - if =='', use repo_uoa


            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              dict         - final dict with key 'features'={...} 
            }

    """

    import os
    import json

    o=i.get('out','')
    oo=''
    if o=='con':oo=o

    muoa=cfg['module_deps']['program']
    duoa=i.get('data_uoa','')
    ruoa=i.get('repo_uoa','')

    truoa=i.get('target_repo_uoa','')

    tags=i.get('tags','')

    rx=ck.access({'action':'search',
                  'repo_uoa':ruoa,
                  'module_uoa':muoa,
                  'data_uoa':duoa,
                  'tags':tags})
    if rx['return']>0: return rx

    lst=rx['lst']

    feat1={}

    num=0
    for q in lst:
        num+=1

        duid=q['data_uid']
        duoa=q['data_uoa']

        xtruoa=truoa
        if truoa=='':
           xtruoa=q['repo_uid']

        if o=='con':
           ck.out(str(num)+') Processing '+duoa+' ...')

        ii={'action':'pipeline',
            'module_uoa':muoa,
            'data_uoa':duoa,
            'milepost':'yes',
            'out':oo,
            'quiet':'yes',
            'skip_info_collection':'yes',
            'no_run':'yes'}
        r=ck.access(ii)
        if r['return']>0:
           if o=='con':
              ck.out('')
              ck.out('CK WARNING: pipeline failed ('+r['error']+')')
              ck.out('')
        else:
           feat=r.get('features',{}).get('program_static_milepost_features',{})

           if len(feat)>0:

              ddd={}

              found=False
              ry=ck.access({'action':'load',
                            'module_uoa':work['self_module_uid'],
                            'data_uoa':duid})
              if ry['return']==0: 
                 ddd=ry['dict']
                 found=True

              feat1=ddd.get('features',{}).get('program_static_milepost_features',{})
              rz=ck.merge_dicts({'dict1':feat1, 'dict2':feat})
              if rz['return']>0: return rz
              feat1=rz['dict1']

              if 'features' not in ddd: ddd['features']={}

              ddd['features']['program_static_milepost_features']=feat1

              ii={}
              ii['action']='add'
              if found: ii['action']='update'
              ii['module_uoa']=work['self_module_uid']
              ii['data_uoa']=duoa
              ii['data_uid']=duid
              ii['repo_uoa']=xtruoa
              ii['dict']=ddd
              ii['substitute']='yes'
              ry=ck.access(ii)
              if ry['return']>0: return ry

    return {'return':0, 'dict':{'features':feat1}}

##############################################################################
# Calculate similarity between programs based on features
#
# FGG: For now just simple Euclidean distance, however it has many drawbacks
# since it doesn't take into account "importance" of different features, etc
# We plan to use more SVN, decision trees, etc (see our papers) ...

def calculate_similarity(i):
    """
    Input:  {
              features1 - MILEPOST features for program 1
              features2 - MILEPOST features for program 2
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              distance     - basic Euclidean distance (can be > 1)
            }

    """

    import math

    prog1=i['features1']
    prog2=i['features2']

    # Check which feature to use for normalization
    fd=cfg['milepost_features_description']
    ftn=cfg['milepost_normalization_feature']

    # Check that in vectors
    distance=None # if error

    if ftn in prog1 and ftn in prog2:

       ftnp1=float(prog1[ftn])
       ftnp2=float(prog2[ftn])

       distance=0.0
       
       for q2 in fd:
           q=fd[q2]

           ftp1=float(prog1.get(q2,0))
           ftp2=float(prog2.get(q2,0))

           if q.get('use_for_euclidean_distance','')=='yes':
              if q.get('normalized','')!='yes':
                 ftp1/=ftnp1
                 ftp2/=ftnp2

              distance+=(ftp1-ftp2)*(ftp1-ftp2)

       if distance!=0.0:
          distance=math.sqrt(distance)

    return {'return':0, 'distance':distance}
