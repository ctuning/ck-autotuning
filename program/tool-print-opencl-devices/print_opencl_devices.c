#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#define MAX_NUM_PLATFORMS (0xF)
#define MAX_WORK_ITEM_DIMENSIONS (0x3)

int main(int argc, char *argv[]) {

    cl_int err = CL_SUCCESS;

    char* value;
    size_t valueSize;

    cl_uint platformCount;
    cl_platform_id* platforms;
    cl_uint p;

    cl_uint deviceCount;
    cl_device_id* devices;
    cl_uint d;

    cl_bool unifiedMemory; // Grigori added on 20171004 to support recompilation of Caffe and other frameworks with OpenCL support
    cl_uint addressBits;
    cl_uint maxComputeUnits;
    cl_uint maxWorkItemDimensions;
    size_t maxWorkItemSizes[MAX_WORK_ITEM_DIMENSIONS];

    FILE* fout=NULL;

    if (argc>1) {
       printf("\nOutput file: %s\n", argv[1]);
       fout=fopen(argv[1], "w");
       fprintf(fout, "{\n");
    }

    // get all platforms

    // platformCount = min(number of available platforms, MAX_NUM_PLATFORMS)
    err = clGetPlatformIDs(MAX_NUM_PLATFORMS, NULL, &platformCount);
    assert(CL_SUCCESS == err && platformCount <= MAX_NUM_PLATFORMS);
    platforms = (cl_platform_id*) malloc(sizeof(cl_platform_id) * platformCount);
    assert(platforms);
    err = clGetPlatformIDs(platformCount, platforms, NULL);
    assert(CL_SUCCESS == err);

    for (p = 0; p < platformCount; p++) {

        if (fout!=NULL) fprintf(fout, "  \"%u\":{\n", p);

        // get all devices
        err = clGetDeviceIDs(platforms[p], CL_DEVICE_TYPE_ALL, 0, NULL, &deviceCount);
        assert(CL_SUCCESS == err);
        devices = (cl_device_id*) malloc(sizeof(cl_device_id) * deviceCount);
        assert(devices);
        err = clGetDeviceIDs(platforms[p], CL_DEVICE_TYPE_ALL, deviceCount, devices, NULL);
        assert(CL_SUCCESS == err);

        // for each device print critical attributes
        for (d = 0; d < deviceCount; d++) {

            if (fout!=NULL) fprintf(fout, "    \"%u\":{\n", d);

            printf("Platform ID: %u\n", p);
            printf("Device ID: %u\n", d);

            // print device name
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_NAME, 0, NULL, &valueSize);
                assert(CL_SUCCESS == err);
                value = (char*) malloc(valueSize);
                assert(value);
                err = clGetDeviceInfo(devices[d], CL_DEVICE_NAME, valueSize, value, NULL);
                assert(CL_SUCCESS == err);
                printf("Device: %s\n", value);
                if (fout!=NULL) fprintf(fout, "      \"device_name\":\"%s\",\n", value);
                free(value);
            }

            // print device name
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_VENDOR, 0, NULL, &valueSize);
                assert(CL_SUCCESS == err);
                value = (char*) malloc(valueSize);
                assert(value);
                err = clGetDeviceInfo(devices[d], CL_DEVICE_VENDOR, valueSize, value, NULL);
                assert(CL_SUCCESS == err);
                printf("Vendor: %s\n", value);
                if (fout!=NULL) fprintf(fout, "      \"device_vendor\":\"%s\",\n", value);
                free(value);
            }

            // print hardware device version
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_VERSION, 0, NULL, &valueSize);
                assert(CL_SUCCESS == err);
                value = (char*) malloc(valueSize);
                assert(value);
                err = clGetDeviceInfo(devices[d], CL_DEVICE_VERSION, valueSize, value, NULL);
                assert(CL_SUCCESS == err);
                printf("Hardware (device) version: %s\n", value);
                if (fout!=NULL) fprintf(fout, "      \"hardware_version\":\"%s\",\n", value);
                free(value);
            }

            // print software driver version
            {
                err = clGetDeviceInfo(devices[d], CL_DRIVER_VERSION, 0, NULL, &valueSize);
                assert(CL_SUCCESS == err);
                value = (char*) malloc(valueSize);
                assert(value);
                err = clGetDeviceInfo(devices[d], CL_DRIVER_VERSION, valueSize, value, NULL);
                assert(CL_SUCCESS == err);
                printf("Software (driver) version: %s\n", value);
                if (fout!=NULL) fprintf(fout, "      \"software_version\":\"%s\",\n", value);
                free(value);
            }

            // print c version supported by compiler for device
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_OPENCL_C_VERSION, 0, NULL, &valueSize);
                assert(CL_SUCCESS == err);
                value = (char*) malloc(valueSize);
                assert(value);
                err = clGetDeviceInfo(devices[d], CL_DEVICE_OPENCL_C_VERSION, valueSize, value, NULL);
                assert(CL_SUCCESS == err);
                printf("OpenCL C version: %s\n", value);
                if (fout!=NULL) fprintf(fout, "      \"opencl_c_version\":\"%s\",\n", value);
                free(value);
            }

            // print CL_DEVICE_HOST_UNIFIED_MEMORY
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_HOST_UNIFIED_MEMORY,
                        sizeof(unifiedMemory), &unifiedMemory, NULL);
                assert(CL_SUCCESS == err);
                printf("Unified memory: %s\n", unifiedMemory ? "yes" : "no");
                if (fout!=NULL) fprintf(fout, "      \"unified_memory\":\"%s\"\n", unifiedMemory==CL_TRUE ? "yes" : "no");
            }

            // print address bits
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_ADDRESS_BITS,
                        sizeof(addressBits), &addressBits, NULL);
                assert(CL_SUCCESS == err);
                printf("Address bits: %d\n", addressBits);
                if (fout!=NULL) fprintf(fout, "      \"address_bits\":\"%d\"\n", addressBits);
            }

            // print parallel compute units
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_MAX_COMPUTE_UNITS,
                        sizeof(maxComputeUnits), &maxComputeUnits, NULL);
                assert(CL_SUCCESS == err);
                printf("Parallel compute units: %d\n", maxComputeUnits);
                if (fout!=NULL) fprintf(fout, "      \"parallel_compute_units\":\"%d\"\n", maxComputeUnits);
            }

            // print max work-item dimensions
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_MAX_WORK_ITEM_DIMENSIONS,
                        sizeof(maxWorkItemDimensions), &maxWorkItemDimensions, NULL);
                assert(CL_SUCCESS == err);
                printf("Work-item dimensions: %d\n", maxWorkItemDimensions);
                if (fout!=NULL) fprintf(fout, "      \"max_work_item_dimensions\":\"%d\"\n", maxWorkItemDimensions);
                assert(MAX_WORK_ITEM_DIMENSIONS == maxWorkItemDimensions);
            }

            // print max work-item sizes
            {
                err = clGetDeviceInfo(devices[d], CL_DEVICE_MAX_WORK_ITEM_SIZES,
                        sizeof(maxWorkItemSizes), &maxWorkItemSizes, NULL);
                assert(CL_SUCCESS == err);
                for (cl_uint dim = 0; dim < maxWorkItemDimensions; ++dim)
                {
                    printf("- max work-item size #%d: %d\n", dim, maxWorkItemSizes[dim]);
                    if (fout!=NULL) fprintf(fout, "      \"max_work_item_size_%d\":\"%d\"\n", dim, maxWorkItemSizes[dim]);
                }
            }

            printf("\n");

            if (fout!=NULL) {
               fprintf(fout, "    }");
               if (d!=(deviceCount-1)) fprintf(fout, ",");
               fprintf(fout, "\n");
            }
        }

        if (fout!=NULL) {
           fprintf(fout, "  }");
           if (p!=(platformCount-1)) fprintf(fout, ",");
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
