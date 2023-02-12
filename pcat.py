#!/usr/bin/env python
from colorama import Fore
import sys
import re
import argparse


dict_regex_color: dict = {
    "string": (r"(\".+\")", Fore.LIGHTYELLOW_EX),
    "char": (r"(\'.+\')", Fore.LIGHTYELLOW_EX),
    "function": (r"(\w+)(?=\s?\()", Fore.LIGHTYELLOW_EX),
    "list": (r"(\w+)(?=\s?\[)", Fore.LIGHTYELLOW_EX),
    "digit": (r"(\d+)", Fore.LIGHTYELLOW_EX),
    "keyword": (
        r"(if|elif|else|def|for|while|try|except|class|from|import|return)",
        Fore.GREEN,
    ),
}


def find_and_color(word: str) -> str:
    for key in dict_regex_color:
        regex, color = dict_regex_color[key]
        match = re.search(regex, word)
        if match is not None:
            start, end = match.span()
            line = word[:start] + color + word[start:end] + Fore.WHITE + word[end:]
            return line
    return word


def read_file(filename: str) -> None:
    with open(filename, "r") as file:
        result = file.readlines()
        for word in result:
            line = word.split()
            if len(line) > 0:
                # if line start with #
                if line[0] == "#":
                    sys.stdout.write(Fore.CYAN + word + Fore.WHITE)
                    continue
                else:
                    tabsize = len(word.split("  "))
                    if tabsize >= 1:
                        sys.stdout.write("  " * tabsize)
                    for w in word.split():
                        sys.stdout.write(find_and_color(w) + " ")
            sys.stdout.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("f", type=str, nargs="?")
    args = parser.parse_args()
    filename = args.f

    if filename is not None:
        read_file(filename)
