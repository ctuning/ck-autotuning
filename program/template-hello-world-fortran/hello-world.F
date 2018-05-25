      PROGRAM HELLOWORLD

C
C     CK program template
C
C     See CK LICENSE.txt for licensing details
C     See CK COPYRIGHT.txt for copyright details
C
C     Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
C

      CHARACTER(len=128) :: CK_VAR1
      CHARACTER(len=128) :: CK_VAR2

      CK_VAR1=''
      CALL GETENV("CK_VAR1", CK_VAR1)

      CK_VAR2=''
      CALL GETENV("CK_VAR2", CK_VAR2)

      WRITE (*,*) 'Hello world!'
      WRITE (*,*) ' '

      WRITE (*,*) 'CK_VAR1: ', CK_VAR1
      WRITE (*,*) 'CK_VAR2: ', CK_VAR2

      END
