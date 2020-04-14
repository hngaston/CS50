#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    // condition
    while (h < 1 || h > 8);

    for (int r = 0; r < h; r++)
    {
        // left pyramid
        int i = 0;

        // put the conditional below in a for loop
        for (i = 0; i < h; i++)

            if (i < (h - (r + 1)))
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }


        printf("  ");


        // right pyramid
        for (i = 0; i < (r + 1); i++)
        { 
            printf("#");
        }
        printf("\n");
    }
}
