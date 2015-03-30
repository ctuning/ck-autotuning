/* 
 Codelet from MILEPOST project: http://cTuning.org/project-milepost
 Updated by Grigori Fursin to work with Collective Mind Framework

 3 "./susan.codelet__2.wrapper.c" 3 4
*/

#ifdef OPENME
#include "openme.h"
#endif

#include <stdio.h>

int __astex_write_message(const char * format, ...);
int __astex_write_output(const char * format, ...);
void __astex_exit_on_error(const char * msg, int code, const char * additional_msg);
void * __astex_fopen(const char * name, const char * mode);
void * __astex_memalloc(long bytes);
void __astex_close_file(void * file);
void __astex_read_from_file(void * dest, long bytes, void * file);
int __astex_getenv_int(const char * var);
void * __astex_start_measure();
double __astex_stop_measure(void * _before);
typedef unsigned char  uchar;
void  astex_codelet__2(int *r, uchar *mid, int x_size, int y_size, int l[9], int a, int b);
int main(int argc, const char **argv)
{
  int  *r;
  uchar  *mid;
  int  x_size = 600;
  int  y_size = 450;
  int  *l;
  int  a = -2064027680;
  int  b = -2064027680;
  void * codelet_data_file_descriptor = (void *) 0;

#ifdef OPENME
  if (openme_init(NULL,NULL,NULL,0)!=0) {
    printf("Failed initializing (auto-tuning) plugin framework\n");
    exit(1);
  }
  openme_callback("PROGRAM_START", NULL);
#endif

  if (argc < 2)
    __astex_exit_on_error("Please specify data file in command-line.", 1, argv[0]);
  codelet_data_file_descriptor = __astex_fopen(argv[1], "rb");
  
  char * r__region_buffer = (char *) __astex_memalloc(1080000);
  __astex_write_message("Reading r value from %s\n", argv[1]);
  __astex_read_from_file(r__region_buffer, 1080000, codelet_data_file_descriptor);
  r = (int *) (r__region_buffer + 0l);
  char * mid__region_buffer = (char *) __astex_memalloc(270000);
  __astex_write_message("Reading mid value from %s\n", argv[1]);
  __astex_read_from_file(mid__region_buffer, 270000, codelet_data_file_descriptor);
  mid = (uchar *) (mid__region_buffer + 0l);
  char * l__region_buffer = (char *) __astex_memalloc(36);
  __astex_write_message("Reading l value from %s\n", argv[1]);
  __astex_read_from_file(l__region_buffer, 36, codelet_data_file_descriptor);
  l = (int *) (l__region_buffer + 0l);
  void * _astex_timeval_before = __astex_start_measure();
  int _astex_wrap_loop = __astex_getenv_int("CT_REPEAT_MAIN");
  if (! _astex_wrap_loop)
    _astex_wrap_loop = 1;

#ifdef OPENME
  openme_callback("KERNEL_START", NULL);
#endif

  while (_astex_wrap_loop > 0)
  {
    --_astex_wrap_loop;
  astex_codelet__2(r, mid, x_size, y_size, l, a, b);

  }

#ifdef OPENME
  openme_callback("KERNEL_END", NULL);
#endif

  __astex_write_output("Total time: %lf\n", __astex_stop_measure(_astex_timeval_before));


#ifdef OPENME
  openme_callback("PROGRAM_END", NULL);
#endif

  return 0;
}

