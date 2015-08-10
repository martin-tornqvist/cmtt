#include "framework.h"

#include <stdio.h>

#ifndef TEST_LOG
#error "TEST_LOG must be defined"
#endif

/* This is used to stringify the TEST_LOG path macro */
#define xstr(s) str(s)
#define str(s) #s

static const char* results_path = xstr(TEST_LOG);

static FILE* results_f;

void framework_init()
{     
    /* Overwrite results file with a label */
    results_f = fopen(results_path, "w");

    fprintf(results_f, "Test results:\n");

    fclose(results_f);

    /* Open again in append mode */
    results_f = fopen(results_path, "a");
}

void framework_cleanup()
{
    fclose(results_f);
}

void check(const char* msg, bool test)
{
    const char* result_str = test ? "PASSED" : "FAILED";

    fprintf(results_f, "%s: %s\n", msg, result_str);
}
