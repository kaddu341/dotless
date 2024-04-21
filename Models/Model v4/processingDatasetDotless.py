import random

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
    "ء": "ا",
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

def allVariation(root):
    stack = [(list(root), 0)]
    variations = []

    while stack:
        word, i = stack.pop()
        char = word[i]

        for dot in iLetters[char]:
            word[i] = dot
            if i == len(word) - 1:
                variations.append(''.join(word))
            else:
                stack.append((list(word), i + 1))

    return variations

def parse_dotless_text(text):
  dotless_chars = [letter_dict[char] for char in text]
  dotless_string = ''.join(dotless_chars)
        
  dotless_string = replace(dotless_string, '_')
    
  return dotless_string

def mask_word(text, index=None):
    words = text.split()
    if index == None: index = random.randint(0, len(words) - 1)

    for i, word in enumerate(words):
        if i == index:
            word_to_replace = words[i]
            variations = allVariation(parse_dotless_text(word_to_replace))
            words[i] = "[MASK]"
            modified_string = ' '.join(words)
            masked = (modified_string)
            options = (variations)
            targets = (word_to_replace)

    return {"Masked": masked, "Options": options, "Target": targets}