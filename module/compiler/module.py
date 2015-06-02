#
# Collective Knowledge (compiler choices)
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
# extract choices to universal pipeline tuning

def extract_to_pipeline(i):
    """
    Input:  {
              (data_uoa) - compiler description
              (file_in)  - JSON pipeline template
              (file_out) - output prepared pipeline to this file
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              pipeline     - prepared pipeline
            }

    """

    fo=i.get('file_out','')
    fi=i.get('file_in','')
    duoa=i.get('data_uoa','')

    # Prepare pipeline template
    ck.out('Preparing pipeline template ...')

    if fi=='':
       fi=os.path.join(work['path'],cfg['pipeline_template'])

    r=ck.load_json_file({'json_file':fi})
    if r['return']>0: return r
    pipeline=r['dict']

    # Load or select compiler description
    ck.out('')
    ck.out('Selecting compiler and description ...')
    if duoa=='':
       rx=ck.access({'action':'search',
                     'module_uoa':work['self_module_uid']})
       if rx['return']>0: return rx
       lst=rx['lst']

       if len(lst)==0:
          duoa=''
       elif len(lst)==1:
          duid=lst[0]['data_uid']
          duoa=lst[0]['data_uoa']
       else:
          # SELECTOR *************************************
          ck.out('')
          ck.out('Multiple choices available:')
          ck.out('')
          r=ck.select_uoa({'choices':lst})
          if r['return']>0: return r
          duoa=r['choice']

    if duoa=='':
       return {'return':1, 'error':'no compiler description selected'}

    # Load compiler desc
    rx=ck.access({'action':'load',
                  'module_uoa':work['self_module_uid'],
                  'data_uoa':duoa})
    if rx['return']>0: return rx
    d=rx['dict']
    dsc=rx.get('desc',{})
    
    dx=dsc.get('all_compiler_flags_desc',{})
   
    # Update pipeline
    ck.out('')
    ck.out('Updating pipeline choices with compiler flags ...')

    if 'pipeline' not in pipeline: pipeline['pipeline']={}
    px=pipeline['pipeline']

    px['choices_desc']={}
    for q in dx:
        qq=dx[q]
        q1=q
        if q1.startswith('##'): q1=q1[1:]
        q1='##compiler_flags'+q1
        px['choices_desc'][q1]=qq

    # Saving file
    if fo!='':
       ck.out('')
       ck.out('Writing pipeline ...')

       rx=ck.save_json_to_file({'json_file':fo, 'dict':pipeline})
       if rx['return']>0: return rx

    return {'return':0, 'pipeline':pipeline}
