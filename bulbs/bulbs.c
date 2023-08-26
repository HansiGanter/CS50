#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);
void calcBinary(char c);

int main(void)
{
    string msg = get_string("Message: ");
    for (int i = 0, n = strlen(msg); i < n; i++)
    {
        calcBinary(msg[i]);
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}

void calcBinary(char c)
{
    for (int i = 7; i >= 0; i--)
    {
        print_bulb((c >> i) & 1);
    }
}