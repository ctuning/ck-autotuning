#!/usr/bin/python

#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os
import sys
import json

##############################################################################
# customize installation

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet

              path             - path to entry (with scripts)
              install_path     - installation path
            }

    Output: {
              return        - return code =  0, if successful
                                          >  0, if error
              (error)       - error text if return > 0

              (install_env) - prepare environment to be used before the install script
            }

    """

    import os
    import shutil

    # Get variables
    o=i.get('out','')

    ck=i['ck_kernel']
    del(i['ck_kernel'])
    ck.save_json_to_file({'json_file':'d:\\xyz.json','dict':i})
    exit(1)

    hos=i['host_os_uoa']
    tos=i['target_os_uoa']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hbits=hosd.get('bits','')
    tbits=tosd.get('bits','')

    hname=hosd.get('ck_name','')    # win, linux
    hname2=hosd.get('ck_name2','')  # win, mingw, linux, android
    macos=hosd.get('macos','')      # yes/no

    p=i['path']

    env=i['env']

    pi=i.get('install_path','')

    cus=i['customize']
    ie=cus.get('install_env',{})
    nie={} # new env

    # Update vars
    f=ie['PACKAGE_NAME_TEMPLATE']

    if macos=='yes':
       f+='macosx'
       if hbits=='64':
          f+='-x64.dmg'
       else:
          return {'return':1, 'error':'this package doesn\'t support non 64-bit MacOS'}
    elif hname=='win':
       f+='windows'
       if hbits=='64':
          f+='-x64.exe'
       else:
          f+='-i586.exe'
    else:
       f+='linux'
       if hbits=='64':
          f+='-x64.tar.gz'
       else:
          f+='-i586.tar.gz'

    nie['PACKAGE_NAME']=f

    print (f)
    exit(1)

    return {'return':0, 'install_env':nie}
