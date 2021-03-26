#!/usr/bin/env python3
"""This finds palindromes."""

import argparse
import typing
import words


def get_palindromes(word_list: typing.List[str]):
    palindromes = set()
    for word in word_list:
        if len(word) > 1 and word == word[::-1]:
            palindromes.add(word)
    palindromes = sorted(palindromes)
    return palindromes


def main():
    parser = argparse.ArgumentParser(description='Find palindromes!',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--wordlist', type=str, default='../third-party/12dicts-6.0.2/International/3of6game.txt', required=False,
                        help='Path to plaintext file with one word per line.')
    args = parser.parse_args()
    word_list = words.get_words(args.wordlist)
    palindrome_list = get_palindromes(word_list)

    print("Wordlist count: {}".format(len(word_list)))
    print("Palindrome count: {}".format(len(palindrome_list)))


if __name__ == "__main__":
    main()
