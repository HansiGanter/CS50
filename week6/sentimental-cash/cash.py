# TODO
from cs50 import get_float


def main():
    change = get_float("Change owed: ") * 100
    while change < 0:
        change = get_float("Change owed: ") * 100

    coins = 0
    coins = coins + int(change / 25)
    change = change % 25

    coins = coins + int(change / 10)
    change = change % 10

    coins = coins + int(change / 5)
    change = change % 5

    coins = coins + int(change / 1)
    change = change % 1

    print(coins)


main()
