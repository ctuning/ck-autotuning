#
# Converting raw slambench timing to CK universal 
# autotuning and machine learning format
#
# Collective Knowledge (CK)
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer: Grigori Fursin
#

import json

d={}

print ('  (converting fine-grain energy - A7+mem ; A15+mem ...)')

# Preload tmp-ck-timer.json from OpenME if there
exists=True
try:
  f=open('tmp-ck-timer.json', 'r')
except Exception as e:
  exists=False
  pass

if exists:
   try:
     s=f.read()
     d=json.loads(s)
   except Exception as e:
     exists=False
     pass

   if exists:
      f.close()

rts=d.get('run_time_state',{})

# Note that this energy is (file_0_start + file_0_stop)*execution_time_kernel_0/2
a15=rts.get('file_0_energy','')
mem=rts.get('file_1_energy','')
gpu=rts.get('file_2_energy','')
a7=rts.get('file_3_energy','')

if a15=='': a15=0.0
a15=float(a15)
if mem=='': mem=0.0
mem=float(mem)
if gpu=='': gpu=0.0
gpu=float(gpu)
if a7=='': a7=0.0
a7=float(a7)

rts['energy_a15']=a15
rts['energy_a7']=a7
rts['energy_mem']=mem
rts['energy_gpu']=gpu

rts['energy_a7_mem']=a7+mem
rts['energy_a15_mem']=a15+mem

rts['energy_a7_mem_gpu']=a7+mem+gpu
rts['energy_a15_mem_gpu']=a15+mem+gpu

rts['energy_gpu_mem']=gpu+mem

rts['energy_a7_a15_mem_gpu']=a15+a7+mem+gpu

d['run_time_state']=rts

# Write CK json
f=open('tmp-ck-timer.json','wt')
f.write(json.dumps(d, indent=2, sort_keys=True)+'\n')
f.close()
