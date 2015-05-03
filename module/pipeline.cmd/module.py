#
# Collective Knowledge (pipeline demo)
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
# run pipeline

def pipeline(i):
    """
    Input:  {
               (cmd)            - cmd
               (compiler_vars)  - will substitute dummies $#VAR#$ in cmd
               (compiler_flags) - assemble into string and substitute $#compiler_flags#$
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import json
    import os

    o=i.get('out','')

    cmd=i.get('cmd','')

    cv=i.get('compiler_vars',{})
    cf=i.get('compiler_flags',{})
    cdesc=i.get('choices_desc',{})

    if o=='out':
       ck.out('')
       ck.out('         Pipeline started')
       ck.out('')
       ck.out('         Input "compiler_vars"  ='+json.dumps(cv))
       ck.out('         Input "compiler_flags" ='+json.dumps(cf))
       ck.out('         Original CMD           ='+cmd)
       ck.out('')

    cflags=''
    for c in cf:
        cx='##compiler_flags#'+c
        cd=cdesc.get(cx,{})
        ep=cd.get('explore_prefix','')
        cc=cf[c]
        if cc!='':
           if cflags!='': cflags+=' '
           cflags+=ep+str(cc)

    cmd=cmd.replace('$#cflags#$', cflags)

    for q in cv:
        qq=cv[q]
        cmd=cmd.replace('$#'+q+'#$', str(qq)) 

    if o=='con':
       ck.out('Prepared CMD:')
       ck.out('')
       ck.out(cmd)

       ck.out('')
       ck.out('Executing:')
       ck.out('')

    lcmd=cmd.split('\n')
    for l in lcmd:
        os.system(l.strip())

    return {'return':0}
