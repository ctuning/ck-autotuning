#
# Collective Knowledge (dataset features)
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
# extract dataset features

def extract(i):
    """
    Input:  {
              (repo_uoa)        - repository UOA
              (data_uoa)        - dataset UOA (can be wildcards)

              (tags)            - tags to process specific datasets

              (target_repo_uoa) - repo, where to save features


            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import json

    o=i.get('out','')

    muoa=cfg['module_deps']['dataset']
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

    for q in lst:
        duid=q['data_uid']
        duoa=q['data_uoa']

        if o=='con':
           ck.out('Processing '+duoa+' ...')

        rx=ck.access({'action':'load',
                      'module_uoa':muoa,
                      'data_uoa':duoa})
        if rx['return']>0: return rx

        d=rx['dict']
        p=rx['path']

        df=d.get('dataset_files','')
        dt=d.get('tags','')

        feat={}

        ddd={'tags':tags, 'dataset_uid':duid, 'dataset_uoa':duoa}

        ts=0
        for f in df:
            p1=os.path.join(p,f)
            if os.path.isfile(p1):
               ts+=os.path.getsize(p1)

        if ts!=0: feat['total_size']=ts

        if 'image' in dt:
           if o=='con':
              ck.out('  Image detected.')

              for f in df:
                  p1=os.path.join(p,f)
                  if os.path.isfile(p1):
                     try:
                       from PIL import Image
                       im = Image.open(p1)

                       feat['mode']=str(im.mode)
                       feat['format']=str(im.format)
                       feat['width']=im.size[0]
                       feat['height']=im.size[1]

                       inf=im.info
                       feat['compression']=inf.get('compression','')
                       dpi=inf.get('dpi',[])
                       if len(dpi)>1:
                          feat['xdpi']=dpi[0]
                          feat['ydpi']=dpi[1]
                       
                       feat['raw_info']=im.info
                     except Exception as e: 
                        pass

        if len(feat)>0:
           ck.out('  '+json.dumps(feat))

           found=False
           ry=ck.access({'action':'load',
                         'module_uoa':work['self_module_uid'],
                         'data_uoa':duid})
           if ry['return']==0: 
              ddd=ry['dict']              
              found=True

           feat1=ddd.get('features',{})
           rz=ck.merge_dicts({'dict1':feat1, 'dict2':feat})
           if rz['return']>0: return rz
           feat1=rz['dict1']

           ddd['features']=feat1

           ii={}
           ii['action']='add'
           if found: ii['action']='update'
           ii['module_uoa']=work['self_module_uid']
           ii['data_uoa']=duoa
           ii['data_uid']=duid
           ii['repo_uoa']=truoa
           ii['dict']=ddd
           ry=ck.access(ii)
           if ry['return']>0: return ry

    return {'return':0}
