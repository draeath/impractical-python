import re


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
    with open(filename) as file:
        return_words = set()
        for line in file.read().splitlines():
            if __is_invalid_word(word=line):
                continue
            return_words.add(line.lower())
    return sorted(return_words)
