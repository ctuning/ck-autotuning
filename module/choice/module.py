#
# Collective Knowledge (deal with choices)
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
# Make next multi-dimensional choice (with state)

def make(i):
    """
    Input:  {
              choices_desc       - dict with description of choices (flat format)
              choices_order      - list of list of flat choice vectors to tune [[],[],...] - 
                                   list of list is needed to be able to enable indedepent 
                                   selection of groups of choices. For example, iterate
                                   over all possible data set sizes + random flags per data set
              choices_selection  - list of dicts with types of selection for each above group
              choices_current    - current vector of choices
              (random_module)    - if !=None, random module with seed
              (pipeline)         - if set, update it with current choices
              (custom_explore)   - enforce exploration params from command line
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              choices_current    - list of updated choices
              choices            - dictionary of flat choices and values
              choices_order      - list of flat choices (to know order if need such as for LLVM opt)
              pipeline           - upated pipeline with choices
                                   also choices and choices_order are added to pipeline
              finish             - if True, iterations are over
            }

    """

    from random import Random

    o=i.get('out','')

    my_random=i.get('random_module',None)
    if my_random==None: my_random=Random()

    finish=False

    cdesc=i['choices_desc']
    corder=i['choices_order']
    csel=i['choices_selection']
    ccur=i['choices_current']

    pipeline=i.get('pipeline',{})
    cexp=i.get('custom_explore',{})

    cd=len(corder)

    # Init current choices
    if len(ccur)==0:
       for c in range(0, cd):
           cx=corder[c]
           cy=[]
           for k in range(0,len(cx)):
               cy.append('')
           ccur.append(cy)

    update=False
    for cx in range(cd-1,-1,-1):
        cc=corder[cx]
        dc=ccur[cx]

        t=csel[cx]

        tp=t.get('type','')
        if cexp.get('type','')!='': tp=cexp['type']

        ti=t.get('iterations','')
        top=t.get('omit_probability','')
        if cexp.get('omit_probability','')!='': zestart=cexp['omit_probability']
        if top=='': top=0.0
        else: top=float(top)

        zestart=t.get('start','')
        if cexp.get('start','')!='': zestart=cexp['start']

        zestop=t.get('stop','')
        if cexp.get('stop','')!='': zestop=cexp['stop']

        zestep=t.get('step','')
        if cexp.get('step','')!='': zestep=cexp['step']

        if tp=='': tp='random'

        ci=t.get('cur_iter','')
        if ci=='': ci=-1
        
        if cx==(cd-1) or update or ci==-1:
           ci+=1

           if ti!='' and ci>=ti:
              ci=0
              update=True
           else:
              update=False

           dvsame=''
           xupdate=False
           for c in range(len(cc)-1,-1,-1):
               cn=cc[c]

               qt=cdesc.get(cn,{})

               yco=qt.get('can_omit','')
               yhc=qt.get('choice',[])
               yep=qt.get('explore_prefix','')
               ytp=qt.get('type','')

               dcc=dc[c]
               if yep!='' and dcc.startswith(yep):
                  dcc=int(dcc[len(yep):])

               if zestart!='': yestart=zestart
               else: yestart=qt.get('explore_start','')
               if zestop!='': yestop=zestop
               else: yestop=qt.get('explore_stop','')
               if zestep!='': yestep=zestep
               else: yestep=qt.get('explore_step','')

               if yestart!='':
                  if ytp=='float':
                     r1=float(yestart)
                     r2=float(yestop)
                     rs=float(yestep)
                  else:
                     r1=int(yestart)
                     r2=int(yestop)
                     rs=int(yestep)

                  rx=(r2-r1+1)/rs

               dv=qt.get('default','')

               # If exploration, set first
               if yestart!='' and (tp=='parallel-loop' or tp=='loop'):
                  dv=r1

               if ci!=0:
                  lcqx=len(yhc)
                  if tp=='random':
                     omit=False
                     if yco=='yes':
                        x=my_random.randrange(0, 1000)
                        if x<(1000.0*top):
                           omit=True

                     if not omit:
                        if lcqx>0:
                           ln=my_random.randrange(0, lcqx)
                           dv=yhc[ln]
                        elif yestart!='':
                             y=my_random.randrange(0,rx)
                             dv=r1+(y*rs)
                         
                  elif tp=='parallel-random': # Change all dimensions at the same time (if explorable)!
                       if yestart!='':
                          if dvsame=='':
                             y=my_random.randrange(0,rx)
                             dvsame=r1+(y*rs)
                          dv=dvsame

                  elif tp=='parallel-loop' or tp=='loop':
                       dv=dcc
                       if tp=='parallel-loop' or c==len(cc)-1 or xupdate:
                          if yestart!='':
                             dv=dcc+rs
                             if dv>r2:
                                dv=r1
                                if tp=='loop': xupdate=True
                                else: 
                                   ci=0
                                   update=True
                             else:
                                xupdate=False

                          else: # normally choice
                             dv=dcc
                             if dv=='':
                                ln=0
                             else:
                                ln=yhc.index(dv)
                                ln+=1
                             if ln<lcqx:
                                dv=yhc[ln]
                                xupdate=False
                             else:
                                dv=''
                                if tp=='loop': xupdate=True
                                else:
                                   ci=0
                                   update=True

                  # Machine learning based probabilistic adaptive sampling of multi-dimensional 
                  # design and optimization speaces via external plugin
                  # See our work on Probabilistic Source-Level Optimisation of Embedded Programs (2005) and Collective Mind (2014)
                  elif tp=='machine-learning-based' or tp=='model-based' or tp=='adaptive' or tp=='plugin-based' or tp=='customized': 
                       print 'TBD: need to add CK plugin ...'
                         







                  else:
                     return {'return':1, 'error':'unknown autotuning type ('+tp+')'}
                           
               if yep!='' and dv!='': dv=yep+str(dv)
               dc[c]=dv

           if xupdate:
              update=True

        t['cur_iter']=ci

    corder1=[]
    ccur1={}

    if update: # means that all loops were updated
       finish=True 
    else:
       if o=='con': 
          ck.out('')
          ck.out('  Vector of flattened and updated choices:')

       for q in range(0, len(corder)):
           qq=corder[q]
           vq=ccur[q]
           for q1 in range(0, len(qq)):
               qq1=qq[q1]
               vq1=vq[q1]

               corder1.append(qq1)
               ccur1[qq1]=vq1

               if o=='con':
                  if vq1!='':
                     ck.out('    '+qq1+'='+str(vq1))

               rx=ck.set_by_flat_key({'dict':pipeline, 'key':qq1, 'value':vq1})
               if rx['return']>0: return rx
               pipeline=rx['dict']

           # Flatten choices and values, and add to pipeline
           # Useful if order of choices is important (say opt flags in LLVM)
           # Will be decoded by a given pipeline, if needed 
           pipeline['choices_order']=corder1
#           pipeline['choices']=ccur1   

    return {'return':0, 'choices_current':ccur, 'choices_order':corder1, 'choices':ccur1, 'pipeline':pipeline, 'finish':finish}

##############################################################################
# select list

def select_list(i):
    """
    Input:  {
              choices      - simple text list of choices
              (skip_enter) - if 'yes', do not select 0 when entering 0
            }

    Output: {
              return  - return code =  0, if successful
                                    >  0, if error
              (error) - error text if return > 0
              choice  - selected text
            }

    """

    se=i.get('skip_enter','')

    lst=i.get('choices',[])

    zz={}
    iz=0
    for z in lst:
        zs=str(iz)
        zz[zs]=z

        ck.out(zs+') '+z)

        iz+=1

    ck.out('')
    y='Choose first number to select item'
    if se!='yes': y+=' (or press Enter for 0)'
    y+=': '

    rx=ck.inp({'text':y})
    x=rx['string'].strip()
    if x=='' and se!='yes': x='0' 

    if x not in zz:
       return {'return':1, 'error':'number is not recognized'}

    dduoa=zz[x]

    return {'return':0, 'choice':dduoa}