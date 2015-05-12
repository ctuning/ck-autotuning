#include <stdio.h>                                                                                                                                              
#include <stdlib.h>
#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif
 
int main(int argc, char *argv[]) {
 
    int i, j;
    char* value;
    size_t valueSize;
    cl_uint platformCount;
    cl_platform_id* platforms;
    cl_uint deviceCount;
    cl_device_id* devices;
    cl_uint maxComputeUnits;

    FILE* fout=NULL;

    if (argc>1) {
       printf("\nOutput file: %s\n", argv[1]);
       fout=fopen(argv[1], "w");
       fprintf(fout, "{\n");
    }

    // get all platforms
    clGetPlatformIDs(0, NULL, &platformCount);
    platforms = (cl_platform_id*) malloc(sizeof(cl_platform_id) * platformCount);
    clGetPlatformIDs(platformCount, platforms, NULL);
 
    for (i = 0; i < platformCount; i++) {
 
        printf("*******************************************\n");
        printf("Platform: %u\n\n", i);

        if (fout!=NULL) fprintf(fout, "  \"%u\":{\n", i);

        // get all devices
        clGetDeviceIDs(platforms[i], CL_DEVICE_TYPE_ALL, 0, NULL, &deviceCount);
        devices = (cl_device_id*) malloc(sizeof(cl_device_id) * deviceCount);
        clGetDeviceIDs(platforms[i], CL_DEVICE_TYPE_ALL, deviceCount, devices, NULL);
 
        // for each device print critical attributes
        for (j = 0; j < deviceCount; j++) {
 
            if (fout!=NULL) fprintf(fout, "    \"%u\":{\n", j);

            // print device name
            clGetDeviceInfo(devices[j], CL_DEVICE_NAME, 0, NULL, &valueSize);
            value = (char*) malloc(valueSize);
            clGetDeviceInfo(devices[j], CL_DEVICE_NAME, valueSize, value, NULL);
            printf("%d. Device: %s\n", j, value);
            if (fout!=NULL) fprintf(fout, "      \"device_name\":\"%s\",\n", value);

            free(value);
 
            // print hardware device version
            clGetDeviceInfo(devices[j], CL_DEVICE_VERSION, 0, NULL, &valueSize);
            value = (char*) malloc(valueSize);
            clGetDeviceInfo(devices[j], CL_DEVICE_VERSION, valueSize, value, NULL);
            printf(" %d.%d Hardware version: %s\n", j, 1, value);
            if (fout!=NULL) fprintf(fout, "      \"hardware_version\":\"%s\",\n", value);
            free(value);
 
            // print software driver version
            clGetDeviceInfo(devices[j], CL_DRIVER_VERSION, 0, NULL, &valueSize);
            value = (char*) malloc(valueSize);
            clGetDeviceInfo(devices[j], CL_DRIVER_VERSION, valueSize, value, NULL);
            printf(" %d.%d Software version: %s\n", j, 2, value);
            if (fout!=NULL) fprintf(fout, "      \"software_version\":\"%s\",\n", value);
            free(value);
 
            // print c version supported by compiler for device
            clGetDeviceInfo(devices[j], CL_DEVICE_OPENCL_C_VERSION, 0, NULL, &valueSize);
            value = (char*) malloc(valueSize);
            clGetDeviceInfo(devices[j], CL_DEVICE_OPENCL_C_VERSION, valueSize, value, NULL);
            printf(" %d.%d OpenCL C version: %s\n", j, 3, value);
            if (fout!=NULL) fprintf(fout, "      \"opencl_c_version\":\"%s\",\n", value);
            free(value);
 
            // print parallel compute units
            clGetDeviceInfo(devices[j], CL_DEVICE_MAX_COMPUTE_UNITS,
                    sizeof(maxComputeUnits), &maxComputeUnits, NULL);
            printf(" %d.%d Parallel compute units: %d\n", j, 4, maxComputeUnits);
            if (fout!=NULL) fprintf(fout, "      \"parallel_compute_units\":\"%d\"\n", maxComputeUnits);

            if (fout!=NULL) {
              fprintf(fout, "    }", j);
              if (j!=(deviceCount-1)) fprintf(fout, ",");
              fprintf(fout, "\n");
            }
        }

            if (fout!=NULL) {
              fprintf(fout, "  }", j);
              if (i!=(platformCount-1)) fprintf(fout, ",");
              fprintf(fout, "\n");
            }
 
        free(devices);
    }

    if (fout!=NULL) {
       fprintf(fout, "}\n");
       fclose(fout);
    }
 
    free(platforms);
    return 0;
 
}
