#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    double letters = 0;
    double words = 0;
    double sentences = 0;

    string text = get_string("Text: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (tolower(text[i]) < 123 && tolower(text[i]) > 96)
        {
            letters++;
        }
        else if (text[i] == ' ')
        {
            words++;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    words++;

    double index = 0.0588 * ((letters / words) * 100) - 0.296 * ((sentences / words) * 100) - 15.8;
    index = (int) (index + 0.5 - (index < 0));

    if (index < 1)
        printf("Before Grade 1\n");
    else if (index >= 16)
        printf("Grade 16+\n");
    else
        printf("Grade %i\n", (int) index);
}