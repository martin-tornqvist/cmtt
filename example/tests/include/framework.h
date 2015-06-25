#ifndef FRAMEWORK_H
#define FRAMEWORK_H

#include <stdbool.h>

/* A *very* minimal C unit testing "framework" */

void framework_init();

void framework_cleanup();

void check(const char* msg, bool test);

#endif /* FRAMEWORK_H */
