"""This module provides a caching method to access a words list with some basic filtering."""

import re
import base64
import lzma
import json
import os.path


class DataOutdatedError(Exception):
    """Custom exception thrown when original is newer than cached data."""


def __is_duplicate_characters(string: str):
    characters = set()
    for character in string:
        characters.add(character)
    if len(characters) == 1:
        return True
    return False


def __is_invalid_word(word: str, pattern: str = r'^[a-zA-Z]+$', minimum_length: int = 2):
    if len(word) < minimum_length or __is_duplicate_characters(word) or re.fullmatch(pattern, word) is None:
        return True
    return False


def get_words(filename: str):
    """Return a sorted and (somewhat) filtered wordlist from filename. The result is cached."""
    filename_b64 = base64.urlsafe_b64encode(filename.encode()).decode()
    cache_filename = '.get_words__' + filename_b64
    try:
        if os.path.getmtime(cache_filename) <= os.path.getmtime(filename):
            raise DataOutdatedError
        with lzma.open(cache_filename, mode='rt', encoding='utf8') as file:
            return_words = json.load(file)
    except (json.JSONDecodeError, lzma.LZMAError, EOFError, FileNotFoundError, PermissionError, DataOutdatedError):
        with open(filename) as file:
            return_words = set()
            for line in file.read().splitlines():
                if __is_invalid_word(word=line):
                    continue
                return_words.add(line.lower())
        return_words = sorted(return_words)
        with lzma.open(cache_filename, mode='wt', encoding='utf8',
                       format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256, preset=lzma.PRESET_EXTREME) as file:
            json.dump(return_words, file)
    return return_words
