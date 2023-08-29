#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // store key
    int key;
    if (argc == 2 && atoi(argv[1]) != 0)
    {
        bool valid = true;
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            valid = isdigit(argv[1][i]) ? true : false;
        }
        if (valid)
        {
            key = atoi(argv[1]);
        }
        else
        {
            printf("Usage :./ caesar key\n");
            return 1;
        }
    }
    else
    {
        printf("Usage :./ caesar key\n");
        return 1;
    }
    key = key % 26;

    // get plaintext
    string p = get_string("plaintext: ");

    // calculate cyphertext
    printf("ciphertext: ");
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if (p[i] >= 'A' && p[i] <= 'Z')
        {
            if (p[i] + key >= 91)
            {
                printf("%c", p[i] + key - 26);
            }
            else
            {
                printf("%c", p[i] + key);
            }
        }
        else if (p[i] >= 'a' && p[i] <= 'z')
        {
            if (p[i] + key >= 123)
            {
                printf("%c", p[i] + key - 26);
            }
            else
            {
                printf("%c", p[i] + key);
            }
        }
        else
        {
            printf("%c", p[i]);
        }
    }
    printf("\n");
}