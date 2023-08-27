#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // check if only 1 argument
    if (argc != 2)
    {
        printf("Usage :./ substitution KEY\n");
        return 1;
    }

    // check key length
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // check for repeated & non alphabetic characters
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
        for (int j = 0; j < n; j++)
        {
            if (tolower(argv[1][j]) == tolower(argv[1][i]) && i != j)
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    string key = argv[1];

    // get plaintext
    string p = get_string("plaintext: ");

    // encrypt
    printf("ciphertext: ");
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if (p[i] >= 'A' && p[i] <= 'Z')
            printf("%c", toupper(key[p[i] - 65]));
        else if (p[i] >= 'a' && p[i] <= 'z')
            printf("%c", tolower(key[p[i] - 97]));
        else
            printf("%c", p[i]);
    }
    printf("\n");
}