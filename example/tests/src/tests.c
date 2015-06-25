#include <stdio.h>

#include "framework.h"

#include "example_header_1.h"

int main()
{
    framework_init();

    int avg1 = average(2, 10);

    check("Average calculated correctly", avg1 == 6);

    int avg2 = average(-1, 7);

    check("Average with negative value calculated correctly", avg2 == 3);

    int low = lowest(4, -1, 79);

    check("Lowest calculated correctly", low == -1);

    framework_cleanup();
}
