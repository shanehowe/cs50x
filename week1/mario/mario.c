#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Initialise height variable
    int height;

    // Promt user for height until valid input is given
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Print pyramid
    for (int i = 1; i < height + 1; i++)
    {
        for (int k = height; k > i; k--)
        {
            printf(" ");
        }
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

    return 0;
}