#
# Collective Knowledge (pipeline demo)
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

    cpu_freq=str(i.get('cpu_freq',''))
    gpu_freq=str(i.get('gpu_freq',''))

    cv=i.get('compiler_vars',{})
    cf=i.get('compiler_flags',{})

    if o=='con':
       ck.out('')
       ck.out('         Pipeline started')
       ck.out('')
       ck.out('         Input "compiler_vars"  ='+json.dumps(cv))
       ck.out('         Input "compiler_vars"  ='+json.dumps(cv))
       ck.out('         Input "cpu_freq"       ='+cpu_freq)
       ck.out('         Input "gpu_freq"       ='+gpu_freq)
       ck.out('         Original CMD           ='+cmd)
       ck.out('')

    cflags=''
    for c in cf:
        cx='##compiler_flags#'+c
        cc=cf[c]
        if cc!='':
           if cflags!='': cflags+=' '
           cflags+=str(cc)

    cmd=cmd.replace('$#cflags#$', cflags)

    cmd=cmd.replace('$#cpu_freq#$', cpu_freq)
    cmd=cmd.replace('$#gpu_freq#$', gpu_freq)

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
