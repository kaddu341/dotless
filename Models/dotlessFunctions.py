import random
from transformers import AutoTokenizer, AutoModelForMaskedLM
from datasets import load_from_disk
import numpy as np
import torch

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

def parse_dotless_text(text):
  dotless_chars = [letter_dict[char] for char in text]
  dotless_string = ''.join(dotless_chars)
        
  dotless_string = replace(dotless_string, '_')
    
  return dotless_string

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



def get_candidate_word_probabilities(input_text, candidate_words, model, tokenizer):
    tokenized_text = tokenizer.tokenize(input_text)
    masked_word_index = tokenized_text.index('[MASK]')
    input_ids = tokenizer.convert_tokens_to_ids(tokenized_text)
    input_ids = torch.tensor(input_ids, dtype=torch.long).unsqueeze_(0)

    with torch.no_grad():
        output = model(input_ids)

    predictions = output.logits[0, masked_word_index].softmax(dim=0)

    # Tokenize and convert all candidate words to ids at once
    candidate_word_ids = tokenizer.convert_tokens_to_ids(candidate_words)

    # Use a list comprehension to populate the dictionary
    candidate_probabilities = {word: predictions[word_id].item() for word, word_id in zip(candidate_words, candidate_word_ids)}

    return candidate_probabilities

def structured_probabilties(example, model, tokenizer):
    input_text = example["Masked"]
    candidates = example["Options"]

            
    word_probabilities = get_candidate_word_probabilities(input_text, candidates, model, tokenizer)

    sorted_words = sorted(word_probabilities, key=word_probabilities.get, reverse=True)
    most_probable_word = sorted_words[0]

    return word_probabilities, sorted_words, most_probable_word


def easy_test(sentance, model, tokenizer, index=None):
    example = mask_word(sentance, index)
    word_probabilities, sorted_words, most_probable_word = structured_probabilties(example, model, tokenizer)
    print("Length of words:", len(sorted_words))
    for word in sorted_words:
        probability = word_probabilities[word]
        print(f"Word: '{word}', Probability: {probability:.10f}")
        
    print()

    print("Most probable word:", most_probable_word)
    print("Target word:", example["Target"])
    print("------------------------------------------")

    for i in range(len(sorted_words)):
        if sorted_words[i] == example["Target"]:
            print("Sucess at probability level:", i)
            break
    sucess_level = i

