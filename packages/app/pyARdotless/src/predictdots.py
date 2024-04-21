from .utils import iLetters, allVariation, parse_dotless_text, mask_word
import numpy as np
from tashaphyne.stemming import ArabicLightStemmer
from transformers import AutoTokenizer, TFAutoModelForMaskedLM
import tensorflow as tf
from pprint import pprint as pprint

def load_rootlist():
    with open("roots.txt", 'r') as file:
        rootlist = set(file.read().split())
    return rootlist

def load_arwiki():
    with open("arwiki.wordlist", 'r') as file:
        arDictionary = set(file.read().split())
    return arDictionary


def get_candidate_word_probabilities(input_text, candidate_words, tokenizer, model, ArListem):
    tokenized_text = tokenizer.tokenize(input_text)
    masked_word_index = tokenized_text.index('[MASK]')
    input_ids = tokenizer.convert_tokens_to_ids(tokenized_text)
    
    input_ids = tf.constant([input_ids], dtype=tf.int32)  # tf.constant automatically adds batch dimension
    
    # Perform prediction
    output = model(input_ids)
    
    # Extract logits for the masked word and apply softmax
    predictions = tf.nn.softmax(output.logits[0, masked_word_index])

    # Tokenize and verify candidate words
    pre_tokenized_candidate_words = [tokenizer.tokenize(word) for word in candidate_words]
    tokenized_candidate_words = []
    verified_words = []
    for word in pre_tokenized_candidate_words:
        rep_word = candidate_words[pre_tokenized_candidate_words.index(word)]
        if len(word) == 1:
            tokenized_candidate_words.append(word[0])
            verified_words.append(rep_word)
        else:
            #if rep_word not in arDictionary: continue
            stem = ArListem.light_stem(rep_word)
            root = ArListem.get_root()
            
            if len(tokenizer.tokenize(stem)) == 1:
                tokenized_candidate_words.append(tokenizer.tokenize(stem)[0])
                verified_words.append(rep_word)
                
            elif len(tokenizer.tokenize(root)) == 1:
                tokenized_candidate_words.append(tokenizer.tokenize(root)[0])
                verified_words.append(rep_word)
   
    # Convert tokens to IDs
    candidate_word_ids = [tokenizer.convert_tokens_to_ids([word]) for word in tokenized_candidate_words]

    # Calculate probabilities for each candidate word
    candidate_probabilities = {word: predictions[word_id].numpy() for word, word_id in zip(verified_words, candidate_word_ids)}

    return candidate_probabilities

def generate_probabilties(example, tokenizer, model, ArListem, gen_prob_func=get_candidate_word_probabilities):
    input_text = example["Masked"]
    candidates = example["Options"]

    word_probabilities = gen_prob_func(input_text, candidates, tokenizer, model, ArListem)

    sorted_words = sorted(word_probabilities, key=word_probabilities.get, reverse=True)
    if len(sorted_words) > 0:
        most_probable_word = sorted_words[0]
    else:
        most_probable_word = None
        #print(example["Target"])

    return word_probabilities, sorted_words, most_probable_word

def single_test(tokenizer, model, ArListem, specific_string=None, specific_index=None, num_eg=None, gen_prob_func=get_candidate_word_probabilities, example = None):
    if example != None: example = example
    #if num_eg != None: example = dataset['train'][indicies[num_eg]]
    if specific_string != None: example = mask_word(specific_string, specific_index)
    word_probabilities, sorted_words, most_probable_word = generate_probabilties(example, tokenizer, model, ArListem, gen_prob_func)
    print("Length of words:", len(sorted_words))
    for word in sorted_words:
        probability = word_probabilities[word]
        print(f"Word: '{word}', Probability: {probability:.10f}")

    print()

    print("Most probable word:", most_probable_word)
    print("Target word:", example["Target"])
    print("------------------------------------------")

    found = False
    for i in range(len(sorted_words)):
        if sorted_words[i] == example["Target"]:
            print("Sucess at probability level:", i)
            found = True
            sucess_level = i
            break
    if not found: print("Not found.")
    
    pprint(example)
    # print("Masked:", example["Masked"])
    # print("Options:", example["Options"])
    # print("Target:", example["Target"])