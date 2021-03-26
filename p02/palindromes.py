#!/usr/bin/env python3
"""This finds palindromes."""

import argparse
import words


def main():
    parser = argparse.ArgumentParser(description='Find palindromes!',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--wordlist', type=str, default='/var/lib/dict/words', required=False,
                        help='Path to plaintext file with one word per line.')
    args = parser.parse_args()
    wordlist = words.get_words(args.wordlist)


if __name__ == "__main__":
    main()
