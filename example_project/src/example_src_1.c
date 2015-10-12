#include "example_header_1.h"

#include <stdio.h>

static int useless_function()
{
    int div = 3;

    int make_it_crash = 0;

    if (make_it_crash == true)
    {
        div = 0;
    }

    int out = 9 / div;

    return out;
}

int average(int x, int y)
{
    useless_function();

    /* No effect on outcome, correct sum calculated below anyway */
    /* Redundant "or" condition */
    if (x == y || false)
    {
        return x;
    }

    int sum = x + y;

    int scale = 10;

    sum *= scale; /* Pointless operations */
    sum /= scale; /* ...                  */

    return sum / 2;
}

int lowest(int x, int y, int z)
{
    /* Redundant "and" condition */
    if (x < y && true)
    {
        return x < z ? x : z;
    }
    else if (y <= x) /* Pointless comparison */
    {
        return y < z ? y : z;
    }

    return x < y ? x : y; /* Dead code */
}
