/*
 Collective Mind OpenME likwid plugin

 cTuning plugin is used for fine-grain online application timing and tuning

 See cM LICENSE.txt for licensing details.
 See cM Copyright.txt for copyright details.

 Developer(s): Grigori Fursin, started on 2011.09
 http://cTuning.org/lab/people/gfursin

*/

#include <stdio.h>
#include <stdlib.h>
#ifdef __MINGW32__
#include <sys/time.h>
#else
#include <time.h>
#endif

#include <openme.h>
#include <cJSON.h>

#ifndef WINDOWS
#include <dlfcn.h>
#endif

static char buf[1024];
static int ibuf;
static char *bufx;
static char *bufy;
static cJSON *dummy=NULL;
static cJSON *json=NULL;
static cJSON *json1=NULL;
static cJSON *json_str=NULL;

static void kernel_start(void);
static void kernel_end(void);
static void program_start(void);
static void program_end(void);

static char *env;

#include <likwid.h>

extern
#ifdef WINDOWS
__declspec(dllexport) 
#endif
int openme_plugin_init(struct openme_info *oi)
{
  /* FGG: We need next few lines to initialize malloc and free
     for both OpenME and cJSON from user space to be able
     to allocate memory - this is mainly needed for statically
     compiled programs. */
  struct openme_hooks oh;
  cJSON_Hooks jh;

  oh.malloc=oi->hooks->malloc;
  oh.free=oi->hooks->free;
  oh.fopen=oi->hooks->fopen;
  oh.fprintf=oi->hooks->fprintf;
  oh.fseek=oi->hooks->fseek;
  oh.ftell=oi->hooks->ftell;
  oh.fread=oi->hooks->fread;
  oh.fclose=oi->hooks->fclose;
  openme_init_hooks(&oh);

  jh.malloc_fn=oi->hooks->malloc;
  jh.free_fn=oi->hooks->free;
  cJSON_InitHooks(&jh);

  /* Register callbacks */
  openme_register_callback(oi, "KERNEL_START", kernel_start);
  openme_register_callback(oi, "KERNEL_END", kernel_end);
  openme_register_callback(oi, "PROGRAM_START", program_start);
  openme_register_callback(oi, "PROGRAM_END", program_end);

  /* FGG: Dummy call to cJSON to be able to use cJSON functions
     in OpenME library. I do not deallocate it here since compiler
     may perform dead code elimination. However, we should find
     a better way to tell compiler that we will use cJSON
     functions in OpenME ... */
  dummy=cJSON_CreateObject();

  return 0;
}

extern void kernel_start(void)
{
  if ( ((env = getenv(OPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("OpenME event: start kernel\n");

  likwid_markerStartRegion("CMREGION");
}

extern void kernel_end(void)
{
  if ( ((env = getenv(OPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("OpenME event: stop kernel\n");

  likwid_markerStopRegion("CMREGION");
}

extern void program_start(void)
{
  if ( ((env = getenv(OPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("OpenME event: start program\n");

  likwid_markerInit();
}

extern void program_end(void)
{
  if ( ((env = getenv(OPENME_DEBUG)) != NULL) && (atoi(env)==1) )
    printf("OpenME event: ending program\n");

  likwid_markerClose();
}
