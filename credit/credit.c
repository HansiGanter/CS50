#include <cs50.h>
#include <stdio.h>
#include <string.h>

string checkCardType(string nr);
bool luhnsalg(long creditCardNumber);

int main(void)
{
    string output = "INVALID\n";
    long number = get_long("Number: ");
    char cardNr[20];
    sprintf(cardNr, "%ld", number);

    output = checkCardType(cardNr);

    (luhnsalg(number)) ? printf("%s", output) : printf("INVALID\n");
}

string checkCardType(string nr)
{
    // Check AMEX 34, 37
    if ((nr[0] == '3' && ((nr[1] == '4') || (nr[1] == '7'))) && strlen(nr) == 15)
    {
        return "AMEX\n";
    }

    // Check MASTERCARD 51, 52, 53, 54, or 55
    if (nr[0] == '5' && ((nr[1] - '0') >= 1 && (nr[1] - '0') <= 5) && strlen(nr) == 16)
    {
        return "MASTERCARD\n";
    }

    // Check VISA 4
    if (nr[0] == '4' && (strlen(nr) == 13 || strlen(nr) == 16))
    {
        return "VISA\n";
    }
    return "INVALID\n";
}

bool luhnsalg(long creditCardNumber)
{
    int digits[16]; // Assuming maximum of 16 digits for a credit card number
    int len = 0;

    // Extract digits from the credit card number and store in the array
    while (creditCardNumber > 0)
    {
        digits[len] = creditCardNumber % 10;
        creditCardNumber /= 10;
        len++;
    }

    int sum = 0;
    bool alternate = false;

    for (int i = 0; i < len; i++)
    {
        int digit = digits[i];

        if (alternate)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit -= 9;
            }
        }

        sum += digit;
        alternate = !alternate;
    }

    return (sum % 10 == 0);
}