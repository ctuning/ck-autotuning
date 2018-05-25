#
# CK program template
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

def run():

    print ("Hello world")

    print ("")
    print ("CK_VAR1: "+os.environ.get('CK_VAR1',''))
    print ("CK_VAR2: "+os.environ.get('CK_VAR2',''))

    return 0

if __name__ == '__main__':
  exit(run())
