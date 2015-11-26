#include "example_header_1.h"

#include <stdio.h>

static int useless_function()
{
    int div = 3;

    /* To test with mutated program crashing */
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

    /* Pointless operations */
    int scale = 10;
    ++scale;
    --scale;
    sum *= scale;
    sum /= scale;
    scale++;
    scale--;
    ++scale;
    --scale;

    return sum / 2;
}

int lowest(int x, int y, int z)
{
    /* To test with mutated program getting stuck in a loop  */
    while (true)
    {
        int a = 0;
        
        if (a == 0)
        {
            break;
        }
    }

    /* Redundant "and" condition */
    if (x < y && true)
    {
        /* Pointless... */
        x -= 10;

        for (int i = 0; i < 10; ++i)
        {
            ++x;
        }

        return x < z ? x : z;
    }
    else if (y <= x) /* Pointless comparison */
    {
        return y < z ? y : z;
    }

    /* This is dead code */
    return x < y ? x : y;
}
