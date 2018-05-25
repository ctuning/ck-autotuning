/*
 CK program template

 See CK LICENSE.txt for licensing details
 See CK COPYRIGHT.txt for copyright details

 Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
*/

#include <stdio.h>
#include <stdlib.h>

#ifdef XOPENME
#include <xopenme.h>
#endif

int main(int argc, char* argv[])
{
  char* env;

#ifdef XOPENME
  xopenme_init(1,3);
#endif

  printf("Hello world!\n\n");

  env=getenv("CK_VAR1");
  if (env!=NULL) {
    printf("CK_VAR1=%s\n",env);

#ifdef XOPENME
    xopenme_add_var_i(0, "  \"ck_var1\":%u", atoi(env));
#endif
  }

  env=getenv("CK_VAR2");
  if (env!=NULL) {
    printf("CK_VAR2=%s\n",env);

#ifdef XOPENME
    xopenme_add_var_i(1, "  \"ck_var2\":%u", atoi(env));
#endif
  }

  env=getenv("CK_VAR3");
  if (env!=NULL) {
    printf("CK_VAR3=%s\n",env);

#ifdef XOPENME
    xopenme_add_var_i(2, "  \"ck_var3\":%u", atoi(env));
#endif
  }

#ifdef XOPENME
  xopenme_clock_start(0);
#endif

  /* Some calculations */

#ifdef XOPENME
  xopenme_clock_end(0);
#endif

#ifdef XOPENME
  xopenme_dump_state();
  xopenme_finish();
#endif

  return 0;
}
