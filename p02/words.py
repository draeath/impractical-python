"""This module provides a caching method to access a words list with some basic filtering."""

import re
import lzma
import pickle
import os.path
import uuid
import hashlib
import tempfile


class DataOutdatedError(Exception):
    """Custom exception thrown when original is newer than cached data."""


def __is_duplicate_characters(string: str):
    characters = set()
    for character in string:
        characters.add(character)
    if len(characters) == 1:
        return True
    return False


def __is_invalid_word(word: str, minimum_length: int = 2):
    if len(word) < minimum_length or __is_duplicate_characters(word) or re.fullmatch(r'^[a-zA-Z]+$', word) is None:
        return True
    return False


def get_words(filename: str):
    """Return a set of (somewhat) filtered wordlist from filename. The result is cached."""
    cache_node_uuid = uuid.UUID(int=uuid.getnode()).bytes
    cache_hash_input = "words.py|get_words|" + filename
    cache_filename_hash = hashlib.blake2b(cache_hash_input.encode(encoding='utf8'), digest_size=32, key=cache_node_uuid)
    cache_filename = os.path.join(tempfile.gettempdir(), '.' + cache_filename_hash.hexdigest() + '.cache')
    try:
        if os.path.getmtime(cache_filename) <= os.path.getmtime(filename):
            raise DataOutdatedError
        with lzma.open(cache_filename, mode='rb') as file:
            return_words = pickle.load(file)
    except (pickle.UnpicklingError, lzma.LZMAError, EOFError, FileNotFoundError, PermissionError, DataOutdatedError):
        with open(filename) as file:
            return_words = set()
            for line in file.read().splitlines():
                line = line.strip()
                if __is_invalid_word(word=line):
                    word_suffix_match = re.fullmatch(r'^([a-zA-Z]+)([^a-zA-Z]+)$', line)
                    if word_suffix_match is None:
                        continue
                    else:
                        line = word_suffix_match.group(1)
                return_words.add(line.lower())
        with lzma.open(cache_filename, mode='wb', format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256, preset=lzma.PRESET_EXTREME) as file:
            pickle.dump(return_words, file)
    return return_words
