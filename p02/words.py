import re
import base64
import gzip
import pickle


def __is_duplicate_characters(string: str):
    characters = set()
    for character in string:
        characters.add(character)
    if len(characters) == 1:
        return True
    return False


def __is_invalid_word(word: str, pattern: str = r'^[a-zA-Z]+$', minimum_length: int = 2):
    if (len(word) < minimum_length
            or __is_duplicate_characters(word)
            or re.fullmatch(pattern, word) is None):
        return True
    return False


def get_words(filename: str = 'words'):
    filename_b64 = base64.urlsafe_b64encode(filename.encode()).decode()
    cache_filename = '.get_words__' + filename_b64
    try:
        with gzip.open(cache_filename, mode='rb') as file:
            return_words = pickle.load(file)
    except (pickle.UnpicklingError, gzip.BadGzipFile, EOFError, FileNotFoundError, PermissionError):
        with open(filename) as file:
            return_words = set()
            for line in file.read().splitlines():
                if __is_invalid_word(word=line):
                    continue
                return_words.add(line.lower())
        return_words = sorted(return_words)
    # no try/catch here, if it fails we want to know
    with gzip.open(cache_filename, mode='wb', compresslevel=6) as file:
        pickle.dump(return_words, file)
    return return_words
