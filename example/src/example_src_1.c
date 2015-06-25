#include "example_header_1.h"

#include <stdio.h>

static void empty_function()
{
    /* Nothing done here */
}

int average(int x, int y)
{
    empty_function();

    /* No effect on outcome, correct sum calculated below anyway */
    if (x == y)
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
    if (x < y)
    {
        return x < z ? x : z;
    }
    else if (y <= x) /* Pointless comparison */
    {
        return y < z ? y : z;
    }

    return x < y ? x : y; /* Dead code */
}

