/*
 Universal Alchemist low-level plugin to open up any compiler
 for interactive (online) application analysis and tuning

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

#include <string.h>
#include <cJSON.h>
#include <openme.h>

#ifndef WINDOWS
#include <dlfcn.h>
#endif

/************************************* Common vars *************************************/
static char buf[1024];
static char *str=NULL;
static cJSON *json=NULL;
static cJSON *json_str=NULL;

#ifdef WINDOWS
  static clock_t start=0.0, stop=0.0;
#else 
  static double start=0.0, stop=0.0;
  static struct timeval  before, after;
#endif
  static double secs;

/* Alchemist input file environment */
char *alc_env="UNI_ALCHEMIST_INPUT_FILE";

/* Alchemist ini file */
cJSON *j_ini=NULL;

/* Alchemist aggregated output */
char alc_output_file[1024]="";
static cJSON *j_out=NULL;
char alc_input_file[1024]="";
cJSON *j_in=NULL;

cJSON *j_tmp=NULL;
cJSON *j_tmp1=NULL;
cJSON *j_tmp2=NULL;
cJSON *j_tmp3=NULL;
cJSON *j_tmp4=NULL;
cJSON *j_tmp5=NULL;
char *alc_action=NULL;

/************************************* Callbacks *************************************/
struct alc_unroll 
{
  const char *func_name;
  const char *loop_name;
  cJSON *json;  
  int factor;  
};

struct alc_obj
{
  cJSON *json;
  const char *name;
  const char *param;
};

extern void alc_finish(void)
{
  char *env=NULL;

  if ( ((env = getenv("ALC_DEBUG")) != NULL) && (atoi(env)==1) )
     printf("Alchemist Finishing Function: j_out=%p, alc_output_file=%s, j_in=%p, alc_input_file=%s\n", 
        j_out, alc_output_file, j_in, alc_input_file);

  if ((j_out!=NULL) && (strlen(alc_output_file)>0))
     openme_store_json_file(j_out, alc_output_file);

  /* Needed for Open64 but should not be needed for LLVM and GCC */
  if ((j_in!=NULL) && (strlen(alc_input_file)>0))
     openme_store_json_file(j_in, alc_input_file);
}

extern void alc_transform_unroll_init(struct alc_unroll *alc_unroll)
{
//  printf("F=%s L=%s\n", alc_unroll->func_name, alc_unroll->loop_name);

  if (strcmp(alc_action,"record_transformations")==0)
  {
    j_tmp=openme_get_obj(j_out, "transformations");
    if (j_tmp==NULL)
    {
      j_tmp1 = cJSON_CreateObject();
      cJSON_AddItemToObject(j_out, "transformations", j_tmp1);
      j_tmp=openme_get_obj(j_out, "transformations");
    }

    if (strlen(alc_unroll->func_name)==0)
    {
      long no=0;
      j_tmp1=openme_get_obj(j_tmp, "last_no");
      if (j_tmp1!=NULL)
        no=atol(j_tmp1->valuestring);
      sprintf(buf,"%u", no+1);
      j_tmp2 = cJSON_CreateString(buf);
      if (j_tmp1!=NULL)
        cJSON_ReplaceItemInObject(j_tmp, "last_no", j_tmp2);
      else
        cJSON_AddItemToObject(j_tmp, "last_no", j_tmp2);

      sprintf(buf,"%u", no);
      j_tmp3 = cJSON_CreateObject();
      cJSON_AddItemToObject(j_tmp, buf, j_tmp3);
      j_tmp2=openme_get_obj(j_tmp, buf);
    }
    else
    {
      j_tmp1=openme_get_obj(j_tmp, alc_unroll->func_name);
      if (j_tmp1==NULL)
      {
        j_tmp2 = cJSON_CreateObject();
        cJSON_AddItemToObject(j_tmp, alc_unroll->func_name, j_tmp2);
        j_tmp1=openme_get_obj(j_tmp, alc_unroll->func_name);
      }

      j_tmp2=openme_get_obj(j_tmp1, alc_unroll->loop_name);
      if (j_tmp2==NULL)
      {
        j_tmp3 = cJSON_CreateObject();
        cJSON_AddItemToObject(j_tmp1, alc_unroll->loop_name, j_tmp3);
        j_tmp2=openme_get_obj(j_tmp1, alc_unroll->loop_name);
      }
    }

    j_tmp3 = cJSON_CreateString("unroll");
    cJSON_AddItemToObject(j_tmp2, "transformation", j_tmp3); 

    alc_unroll->json=j_tmp2;
  }
  else if (strcmp(alc_action,"apply_transformations")==0)
  {
    if (strlen(alc_unroll->func_name)==0)
    {
      j_tmp=openme_get_obj(j_in, "transformations");
      alc_unroll->json=NULL;
      if (j_tmp!=NULL)
      {
         long no=0;
         j_tmp1=openme_get_obj(j_tmp, "tmp_last_no");
         if (j_tmp1!=NULL)
            no=atol(j_tmp1->valuestring);
         sprintf(buf,"%u", no+1);
         j_tmp2 = cJSON_CreateString(buf);
         if (j_tmp1!=NULL)
           cJSON_ReplaceItemInObject(j_tmp, "tmp_last_no", j_tmp2);
         else
           cJSON_AddItemToObject(j_tmp, "tmp_last_no", j_tmp2);

         sprintf(buf,"%u", no);
         j_tmp2=openme_get_obj(j_tmp, buf);

         alc_unroll->json=j_tmp2;
      }
    }
  }
}

extern void alc_transform_unroll(struct alc_unroll *alc_unroll)
{
  int factor;
//  printf("Event transform unroll\n");
  if (strcmp(alc_action,"record_transformations")==0)
  {
    j_tmp2=alc_unroll->json;
    if (j_tmp2!=NULL)
    {
      sprintf(buf, "%u", alc_unroll->factor);
      j_tmp3 = cJSON_CreateString(buf);
      cJSON_AddItemToObject(j_tmp2, "factor", j_tmp3); 
    }
  }
  else if (strcmp(alc_action,"apply_transformations")==0)
  {
    j_tmp=openme_get_obj(j_in, "transformations");
    if (j_tmp!=NULL)
    {
       j_tmp2=NULL;

       if (strlen(alc_unroll->func_name)==0)
          j_tmp2=alc_unroll->json;
       else
       {
         j_tmp1=openme_get_obj(j_tmp, alc_unroll->func_name);
         if (j_tmp1!=NULL)
            j_tmp2=openme_get_obj(j_tmp1, alc_unroll->loop_name);
       }

       if (j_tmp2!=NULL)
       {
         j_tmp3=openme_get_obj(j_tmp2, "transformation");
         if (j_tmp3!=NULL)
         {
           if (strcmp(j_tmp3->valuestring,"unroll")==0)
           {
             j_tmp4=openme_get_obj(j_tmp2, "factor");
             if (j_tmp4!=NULL)
             {
               factor=atoi(j_tmp4->valuestring);
               printf("Original unroll factor=%u; new factor=%u\n", alc_unroll->factor, factor);
               alc_unroll->factor=factor;
             }
           }
         }
       }
    }
  }
}

extern void alc_transform_unroll_features(struct alc_obj *alc_obj)
{
  if (strcmp(alc_action,"record_transformations")==0)
  {
    j_tmp2=alc_obj->json;
    if (j_tmp2!=NULL)
    {
      j_tmp3 = cJSON_CreateString(alc_obj->param);
      cJSON_AddItemToObject(j_tmp2, alc_obj->name, j_tmp3); 
    }
  }
}

extern void clock_start(void)
{
#ifdef WINDOWS
  start = clock();
#else
  #ifdef __INTEL_COMPILERX
    start = (double)_rdtsc();
  #else
    gettimeofday(&before, NULL);
  #endif
#endif
}

extern void clock_end(void)
{
#ifdef WINDOWS
  stop = clock();
  secs = ((double)(stop - start)) / CLOCKS_PER_SEC;
#else
  #ifdef __INTEL_COMPILERX
  stop = (double)_rdtsc();
  secs = ((double)(stop - start)) / (double) getCPUFreq();
  #else
  gettimeofday(&after, NULL);
  secs = (after.tv_sec - before.tv_sec) + (after.tv_usec - before.tv_usec)/1000000.0;
  #endif
#endif
}

extern void program_start(void)
{
  printf("Event: start program\n");
}

extern void program_end(void)
{
  char *out=NULL;
  char *env=NULL;
  double secs_save=0;

  secs_save=secs;

  if ((env = getenv(OPENME_OUTPUT_FILE)) != NULL)
  {
    sprintf(buf, "run_time_kernel=%f", secs_save);

    json=openme_create_obj(buf);
    if (json==NULL) {openme_print_error(); exit(1);}
    openme_print_obj(json);

    openme_store_json_file(json, env);
  }

  printf("Kernel time in seconds = %f\n", secs_save);
}

/************************************* Plugin init *************************************/

extern
#ifdef WINDOWS
__declspec(dllexport) 
#endif
int openme_plugin_init(struct openme_info *ome_info)
{
  char *env=NULL;

/*  openme_register_callback(ome_info, "KERNEL_START", clock_start);
  openme_register_callback(ome_info, "KERNEL_END", clock_end);
  openme_register_callback(ome_info, "PROGRAM_START", program_start);
  openme_register_callback(ome_info, "PROGRAM_END", program_end); */

  openme_register_callback(ome_info, "ALC_TRANSFORM_UNROLL_INIT", alc_transform_unroll_init);
  openme_register_callback(ome_info, "ALC_TRANSFORM_UNROLL", alc_transform_unroll);

  openme_register_callback(ome_info, "ALC_TRANSFORM_UNROLL_FEATURES", alc_transform_unroll_features);

  openme_register_callback(ome_info, "ALC_FINISH", alc_finish);

  json=cJSON_CreateObject();

  /* Check if file is set */
  str=getenv(alc_env);
  if (str==NULL)
  {
    printf("Alchemist error: environment variable with input file %s is not set !\n", alc_env);
    exit(1);
  }

  alc_action=alc_input_file;

  /* If we want to use openme functions here, we need to initialize OpenMe
     - however it seems to be needed only for Windows */
#ifdef WINDOWS
  openme_init (NULL,NULL,NULL,-1);
#endif

  /* Reading Alchemist input file */
  if ( ((env = getenv("ALC_DEBUG")) != NULL) && (atoi(env)==1) )
     printf("Loading Alchemist ini file %s ...\n", str);

  j_ini=openme_load_json_file(str);
  if (j_ini==NULL)
  {
    printf("Alchemist error: failed to load json file %s !\n", str);
    exit(1);
  }

  /* Process actions */
  j_tmp=openme_get_obj(j_ini, "action");
  if (j_tmp==NULL)
  {
    printf("Alchemist error: failed to load json file %s !\n", str);
    exit(1);
  }

  alc_action=j_tmp->valuestring;

  /* Check if there are input and output files */
  j_tmp=openme_get_obj(j_ini, "input_file");
  if (j_tmp!=NULL)
     strcpy(alc_input_file, j_tmp->valuestring);

  j_tmp=openme_get_obj(j_ini, "output_file");
  if (j_tmp!=NULL)
     strcpy(alc_output_file, j_tmp->valuestring);

  /* Check actions */
  if (strcmp(alc_action, "record_transformations")==0)
  {
     j_out=openme_load_json_file(alc_output_file);
     if (j_out==NULL)
        j_out = cJSON_CreateObject();
  }
  else if (strcmp(alc_action, "apply_transformations")==0)
  {
     j_in=openme_load_json_file(alc_input_file);
     if (j_in==NULL)
     {
       printf("Alchemist error: failed to load json file %s !\n", alc_input_file);
       exit(1);
     }
  }

  return 0;
}
