# TODO
#  MASTERCARD\n  INVALID\n


def main():
    card_number = input("Number: ")

    if len(card_number) not in [13, 15, 16]:
        print("INVALID")

    if luhn(card_number):
        if card_number[:1] == "4":
            print("VISA")
            return
        elif card_number[:2] == "34" or card_number[:2] == "37":
            print("AMEX")
            return
        elif int(card_number[:2]) >= 51 and int(card_number[:2]) <= 55:
            print("MASTERCARD")
            return

    print("INVALID")
    return


def luhn(card_number):
    digits = [int(digit) for digit in reversed(str(card_number))]
    doubled_digits = [
        2 * digit if index % 2 == 1 else digit for index, digit in enumerate(digits)
    ]
    total = sum([(digit // 10 + digit % 10) for digit in doubled_digits])
    return total % 10 == 0


main()
