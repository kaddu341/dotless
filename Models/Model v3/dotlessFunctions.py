
import numpy as np
import re
import sys
import random

def parse_text(text):
  text = text.strip()
  
  clean_chars = [char for char in text if char in letter_set]
  clean_string = ''.join(clean_chars)

  output_chars = [letter_dict[char] for char in clean_chars]
  output_string = ''.join(output_chars)
      
  clean_string = replace(clean_string, ' ')
  output_string = replace(output_string, '_')
  
  return(clean_string, output_string)

# Replaces multiple spaces, or whatever char designated by the perameter into one char. (helper function)
def replace(string, char):
    while char+char in string:
        string = string.replace(char+char, char)

    return string

def reverse_dict_with_duplicates(input_dict):
    reversed_dict = {}
    
    for key, value in input_dict.items():
        if value not in reversed_dict:
            reversed_dict[value] = [key]
        else:
            reversed_dict[value].append(key)
    
    return reversed_dict

letter_dict = {
    "ا": "ا",
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ب": "ب",
    "ت": "ب",
    "ث": "ب",
    "ج": "ح",
    "ح": "ح",
    "خ": "ح",
    "د": "د",
    "ذ": "د",
    "ر": "ر",
    "ز": "ر",
    "س": "س",
    "ش": "س",
    "ص": "ص",
    "ض": "ص",
    "ط": "ط",
    "ظ": "ط",
    "ع": "ع",
    "غ": "ع",
    "ف": "ف",
    "ق": "ف",
    "ك": "ك",
    "ل": "ل",
    "م": "م",
    "ن": "ن",
    "و": "و",
    "ؤ": "و",
    "ه": "ه",
    "ة": "ه",
    "ي": "ى",
    "ى": "ى",
    "ئ": "ى",
    " ": "_",
    
}
letter_set = set(letter_dict.keys())
iLetters = reverse_dict_with_duplicates(letter_dict)

def allVariation(root, i = 0):
    tWord = []
    word = [a for a in root]
    char = word[i]
    for dot in iLetters[char]:
        word[i] = dot
        vWord = ''.join(word)
        if i != len(word) - 1:
            tWord.extend(allVariation(vWord, i+1))
        else:
            #if vWord in dictionary:
            tWord.append(vWord)
    return tWord

def mask_random_word(input_string, seed=None):
    words = input_string.split()
    print(words)
    if seed is not None:
        random.seed(seed)

    if words:
        index = random.randint(0, len(words) - 1)
        word_to_replace = words[index]
        words[index] = "[MASK]"
        modified_string = ' '.join(words)
        return modified_string, word_to_replace
    else:
        return input_string, None