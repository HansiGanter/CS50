#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    } while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            (j < height - i - 1) ? printf(" ") : printf("#");
        }
        printf("  ");
        for (int k = 0; k < height; k++)
        {
            if (k > i)
            {
                printf("\n");
                break;
            }
            else
            {
                printf("#");
            }
        }
    }
    printf("\n");
}