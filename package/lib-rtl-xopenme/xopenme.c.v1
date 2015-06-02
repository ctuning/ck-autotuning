/*

 XOpenME cTuning support run-time library
 (unlike OpenME dynamic plugin framework, this lib is linked directly)

 cTuning plugin is used for fine-grain online application timing and tuning

 OpenME - Event-driven, plugin-based interactive interface to "open up" 
          any software (C/C++/Fortran/Java/PHP) and possibly connect it to cM

 Developer(s): (C) 2015, Grigori Fursin 
 http://cTuning.org/lab/people/gfursin

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef __MINGW32__
# include <sys/time.h>
#else
# ifdef WINDOWS
#  include <time.h>
# else
#  include <sys/time.h>
# endif
#endif

#define XOPENME_DEBUG "XOPENME_DEBUG"

static char* ck_time_file="tmp-ck-timer.json";

#ifdef WINDOWS
# define MYTIMER1 clock_t
 static MYTIMER1 *start;
#else 
# define MYTIMER1 double
# define MYTIMER2 struct timeval
 static MYTIMER1 *start;
 static MYTIMER2 *before, after;
#endif

static double *secs;

static char *env;

static char **vars;

static int nntimers=0;
static int nnvars=0;

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_init(int ntimers, int nvars)
{
  int timer;
  int var;

  if ( ((env = getenv(XOPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("XOPENME event: start program\n");

  nntimers=ntimers;
  nnvars=nvars;

  /* init timers */
  if (ntimers>0)
  {
     secs=malloc((ntimers+1)*sizeof(double));
     start=malloc((ntimers+1)*sizeof(MYTIMER1));
#ifdef MYTIMER2     
     before=malloc(ntimers*sizeof(MYTIMER2));
#endif

     for (timer=0; timer<nntimers; timer++)
     {
       secs[timer] = 0.0;
       start[timer] = 0.0;
     }
  }

  /* init vars */
  if (nvars>0)
  {
    vars=malloc((nvars+1)*sizeof(char*)); 

    for (var=0; var<nvars; var++)
    {

      vars[var]=(char*) malloc(512*sizeof(char)); // temporal and ugly - should check the length ...
      vars[var][0]=0;
    }
  }
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_clock_start(int timer)
{
#ifdef WINDOWS
  start[timer] = clock();
#else
  #ifdef __INTEL_COMPILERX
    start[timer] = (double)_rdtsc();
  #else
    gettimeofday(&before[timer], NULL);
  #endif
#endif
  if ( ((env = getenv(XOPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("XOpenME event: start clock\n");

}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_clock_end(int timer)
{
#ifdef WINDOWS
  secs[timer] = ((double)(clock() - start[timer])) / CLOCKS_PER_SEC;
#else
  #ifdef __INTEL_COMPILERX
  secs[timer] = ((double)((double)_rdtsc() - start[timer])) / (double) getCPUFreq();
  #else
  gettimeofday(&after, NULL);
  secs[timer] = (after.tv_sec - before[timer].tv_sec) + (after.tv_usec - before[timer].tv_usec)/1000000.0;
  #endif
#endif
  if ( ((env = getenv(XOPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("XOpenME event: stop clock: %f\n", secs[timer]);
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_add_var_i(int var, char* desc, int svar)
{
  sprintf(vars[var], desc, svar);
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_add_var_f(int var, char* desc, float svar)
{
  sprintf(vars[var], desc, svar);
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_add_var_d(int var, char* desc, double svar)
{
  sprintf(vars[var], desc, svar);
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_add_var_s(int var, char* desc, void* svar)
{
  sprintf(vars[var], desc, svar);
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_dump_memory(char* name, void* array, long size)
{
  FILE *fx=fopen(name , "wb" );
  fwrite(array, size, 1, fx);
  fclose(fx);
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_dump_state(void)
{
  FILE* f;
  int timer;
  int var;

  if ( ((env = getenv(XOPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("XOPENME event: dumping state\n");

  printf("Stop program\n");

  f=fopen(ck_time_file, "w");
  if (f==NULL)
  {
    printf("Error: can't open timer file %s for writing\n", ck_time_file);
    exit(1);
  }

  fprintf(f,"{\n");

  if (nntimers>0) 
  {
     fprintf(f," \"execution_time\":%.6lf,\n", secs[0]);
     for (timer=0; timer<nntimers; timer++) 
     {
       fprintf(f," \"execution_time_kernel_%u\":%.6lf", timer, secs[timer]);
       if (timer!=(nntimers-1) || (nnvars!=0)) fprintf(f, ",");
       fprintf(f, "\n");
     }
  }

  if (nnvars>0)
  {
    fprintf(f," \"run_time_state\":{\n");
    for (var=0; var<nnvars; var++) 
    {
      if ((vars[var][0]!=0))
      {
         if (var!=0) fprintf(f, ",\n");
         fprintf(f,"  %s", vars[var]);
      }
    }
    fprintf(f,"\n }\n");
  }

  fprintf(f,"}\n");

  fclose(f);
}

/*****************************************************************/
extern 
#ifdef WINDOWS
__declspec(dllexport) 
#endif
void xopenme_finish(void)
{
  int timer;
  int var;

  if (nnvars>0)
  {
    for (var=0; var<nnvars; var++) 
    {
      free(vars[var]);
    }
    free(vars);
  }

  if (nntimers>0)
  {
    free(secs);
    free(start);
#ifdef MYTIMER2
    free(before);
#endif
  }
}
