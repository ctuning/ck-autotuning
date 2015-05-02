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
              choices_desc - 
              choices_dims -
              choices_selection
              choices_current    - current state
              (pipeline)         - if set, update it with current choices
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              choices_current    - updated choices
              (pipeline)         - if set
              finish             - if True, iterations are over
            }

    """

    import random

    o=i.get('out','')

    finish=False

    cdesc=i['choices_desc']
    cdims=i['choices_dims']
    csel=i['choices_selection']
    ccur=i['choices_current']

    pipeline=i.get('pipeline',{})

    cd=len(cdims)

    # Init current choices
    if len(ccur)==0:
       for c in range(0, cd):
           cx=cdims[c]
           cy=[]
           for k in range(0,len(cx)):
               cy.append('')
           ccur.append(cy)

    update=False
    for cx in range(cd-1,-1,-1):
        cc=cdims[cx]
        dc=ccur[cx]

        t=csel[cx]

        tp=t.get('type','')
        ti=t.get('iterations','')
        top=t.get('omit_probability','')
        if top=='': top=0.0
        else: top=float(top)
        zestart=t.get('start','')
        zestop=t.get('stop','')
        zestep=t.get('step','')


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
               if yestart!='' and (tp=='parallel_loop' or tp=='loop'):
                  dv=yestart

               if ci!=0:
                  lcqx=len(yhc)
                  if tp=='random':
                     omit=False
                     if yco=='yes':
                        x=random.randrange(0, 1000)
                        if x<(1000.0*top):
                           omit=True

                     if not omit:
                        if lcqx>0:
                           ln=random.randrange(0, lcqx)
                           dv=yhc[ln]
                        elif yestart!='':
                             y=random.randrange(0,rx)
                             dv=r1+(y*rs)
                         
                  elif tp=='parallel_random': # Change all dimensions at the same time (if explorable)!
                       if yestart!='':
                          if dvsame=='':
                             y=random.randrange(0,rx)
                             dvsame=r1+(y*rs)
                          dv=dvsame

                  elif tp=='parallel_loop' or tp=='loop':
                       dv=dc[c]
                       if tp=='parallel_loop' or c==len(cc)-1 or xupdate:
                          if yestart!='':
                             dv=dc[c]+rs
                             if dv>r2:
                                dv=r1
                                if tp=='loop': xupdate=True
                                else: 
                                   ci=0
                                   update=True
                             else:
                                xupdate=False

                          else: # normally choice
                             dv=dc[c]
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
                  elif tp=='machine-learning-based' or tp=='model' or tp=='adaptive' or tp=='plugin-based' or tp=='customized': 
                       print 'xyz'
                         







                  else:
                     return {'return':1, 'error':'unknown autotuning type ('+tp+')'}
                           
               dc[c]=dv

           if xupdate:
              update=True

        t['cur_iter']=ci

    if update: # means that all loops were updated
       finish=True 
    else:
       if o=='con': 
          ck.out('')
          ck.out('  Vector of flattened and updated choices:')

       cdims1=[]
       ccur1=[]
       for q in range(0, len(cdims)):
           qq=cdims[q]
           vq=ccur[q]
           for q1 in range(0, len(qq)):
               qq1=qq[q1]
               vq1=vq[q1]

               cdims1.append(qq1)
               ccur1.append(vq1)

               if o=='con':
                  if vq1!='':
                     ck.out('    '+qq1+'='+str(vq1))

               rx=ck.set_by_flat_key({'dict':pipeline, 'key':qq1, 'value':vq1})
               if rx['return']>0: return rx
               pipeline=rx['dict']

           # Flatten choices and values, and add to pipeline
           # Useful if order of choices is important (say opt flags in LLVM)
           # Will be decoded by a given pipeline, if needed 
           pipeline['choices_dims']=cdims1
           pipeline['choices']=ccur1   

    return {'return':0, 'choices_current':ccur, 'pipeline':pipeline, 'finish':finish}
