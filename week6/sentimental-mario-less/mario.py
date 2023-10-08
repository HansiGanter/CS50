# TODO
from cs50 import get_int


def main():
    height = get_int("Height: ")
    while height < 1 or height > 8:
        height = get_int("Height: ")

    for i in range(1, height + 1):
        print(" " * (height - i), end="")
        print("#" * i)


main()
