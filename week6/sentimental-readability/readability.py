# TODO
import re


def main():
    text = input("Text: ")

    letters = len(list(filter(lambda char: char.isalpha(), text)))
    words = len(text.split(" "))
    sentences = len(re.split(r"[.!?]\s", text))

    index = round(
        0.0588 * (letters / words * 100) - 0.296 * (sentences / words * 100) - 15.8
    )

    if index < 0:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print("Grade", index)


main()
