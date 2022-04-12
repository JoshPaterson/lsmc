import re
import string
import hunspell
dictionary = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')

modified_punctuation = string.punctuation.replace('-', '')
regex = re.compile(f'[{re.escape(modified_punctuation)}]')

def word_list_to_text(word_list: list):
    words = [word.lower() for word in word_list if word != '']

    words_no_hyphen = []
    skip = False
    for word in words:
        if skip:
            words_no_hyphen[-1] = words_no_hyphen[-1] + word
            skip = False
            continue
        if word[-1] != '-':
            words_no_hyphen.append(word)
        else:
            words_no_hyphen.append(word[:-1])
            skip = True

    words = [regex.sub('', word) for word in words_no_hyphen]
    words = [word for word in words if word != '']
    return ' '.join(words)


def fix_long_s(word):
    if dictionary.spell(word):
        return word
    elif dictionary.spell(word.replace('f', 's')):
        return word.replace('f', 's')
    else:
        return word


def clean_words_long_s(words):
    return [fix_long_s(word) for word in words]
