/*
 CK program template

 See CK LICENSE.txt for licensing details
 See CK COPYRIGHT.txt for copyright details

 Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
  char* env;

  printf("Hello world!\n\n");

  env=getenv("CK_VAR1");
  if (env!=NULL) {
    printf("CK_VAR1=%s\n",env);
  }

  env=getenv("CK_VAR2");
  if (env!=NULL) {
    printf("CK_VAR2=%s\n",env);
  }

  return 0;
}
