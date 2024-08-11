from pyARdotless import *
import numpy as np
import enum
from tqdm import tqdm




# 6 models
models = [
    "CAMeL-Lab/bert-base-arabic-camelbert-mix",
    "bert-base-arabic-camelbert-msa-sixteenth-finetuned-AR-dotted-mediumPlus",
    "UBC-NLP/ARBERT",
    "UBC-NLP/MARBERT",
    "UBC-NLP/MARBERTv2",
    "aubmindlab/bert-large-arabertv2"
]

# 10 examples
arabic_sentences = [
    "أنا أدرس اللغة العربية", 
    "أحب القهوة في الصباح", 
    "الكتاب على الطاولة", 
    "الطقس جميل اليوم", 
    "أسكن في مدينة كبيرة", 
    "أمي تطبخ عشاء لذيذ", 
    "أحب قراءة الكتب", 
    "لديه سيارة جديدة", 
    "نذهب إلى المدرسة كل يوم", 
    "أنا أعمل في شركة كبيرة"
]

benchList = np.zeros(shape = (6, 10))

for i, model_name in tqdm(enumerate(models)):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForMaskedLM.from_pretrained(model_name)
    ArListem = ArabicLightStemmer()
    for j, test_string in tqdm(enumerate(arabic_sentences)):
        word_probabilities, sorted_words, most_probable_word, sucess_level = single_test(
                tokenizer,
                model,
                ArListem,
                specific_string=test_string,
                gen_prob_func=get_candidate_word_probabilities,
            )
        
        benchList[i, j] = sucess_level
        
# average sucess level


for i in range(len(models)):
    print(f"Model: {models[i]}, Average Success Level: {np.mean(benchList[i])}")
    
print("\n\n")

for i in range(len(models)):
    for j in range(len(arabic_sentences)):
        print(f"Model: {models[i]}, Sentence: {arabic_sentences[j]}, Success Level: {benchList[i, j]}")
        
    

        

    
    

        

        
        
        

