#ifndef WINDOWS
 #include <unistd.h>
#endif

#include <stdio.h>

#include <cuda.h>

#define GPU_DEVICE 0

int main(int argc, char *argv[])
{
  int devID = 0;
  cudaError_t error;
  cudaDeviceProp deviceProp;
  error = cudaGetDevice(&devID);

  int runtimeVersion=0;
  int driverVersion=0;

  error=cudaRuntimeGetVersion(&runtimeVersion);
  if (error == cudaSuccess) {
    printf("CUDA runtime version: %d\n", runtimeVersion);
  }

  error=cudaDriverGetVersion(&driverVersion);
  if (error == cudaSuccess) {
    printf("CUDA driver version: %d\n", driverVersion);
  }

  cudaGetDeviceProperties(&deviceProp, GPU_DEVICE);
  if (error == cudaSuccess) {
    printf("GPU Device ID: %d\n", devID);
    printf("GPU Name: %s\n", deviceProp.name);
    printf("GPU compute capability: %d.%d\n", deviceProp.major, deviceProp.minor);
  }
  else {
    printf("Can't initialize CUDA device, return code: %d\n", error);
  }

  return error;
}
