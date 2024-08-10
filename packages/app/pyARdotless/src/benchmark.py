from pyARdotless import *
import numpy as np
from tqdm import tqdm
import pandas as pd
from transformers import AutoTokenizer, TFAutoModelForMaskedLM


def calculateScore(benchList):
    scores = benchList.to_list()
    scores.pop(-1)
    
    print(scores)
    
    negative_count = 0
    total = 0
    for i in range(len(scores)):
        if scores[i] == -1:
            negative_count += 1
        else:
            total += scores[i]

    average = total / ((len(scores) - negative_count)) + 0.001
    average += negative_count
    
    return round(average, 2)

def benchmark(models, arabic_sentences):
     
    benchList = pd.DataFrame(
        columns=models,
    )   

    targets = pd.DataFrame(
        columns=models,
    )
    
    ArListem = ArabicLightStemmer()

    for i, model_name in tqdm(enumerate(models)):
        print(f"---------------[Testing {model_name}]---------------")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = TFAutoModelForMaskedLM.from_pretrained(model_name)
        
        for j, test_string in tqdm(enumerate(arabic_sentences)):
            example, word_probabilities, sorted_words, most_probable_word, sucess_level = (
                single_test(
                    tokenizer,
                    model,
                    ArListem,
                    specific_string=test_string,
                    gen_prob_func=get_candidate_word_probabilities,
                )
            )

            target = example["Target"]
            
            targets.loc[j, model_name] = target
            benchList.loc[j, model_name] = sucess_level
            

            print(f"Sentence: {test_string}, Target: {target}, Success Level: {sucess_level}")
            
        print(len(benchList[model_name].tolist()))
        #remove last item in dataframe
        
        benchList.loc[len(arabic_sentences), model_name] = calculateScore(benchList[model_name])
        print(f"Average Success Level: {benchList.loc[len(arabic_sentences), model_name]}")
        
    # average sucess level

    # print(targets.head())
    # print(benchList.head())


    print("\n\n\n")
    print("---------------[Results]---------------")

    for i in range(len(models)):
        #print last row of benchList
        print(
            f"Model: {models[i]}, Average Success Level: {benchList.loc[len(arabic_sentences), models[i]]}"
        )
        
        
    print("\n\n")

    # for i in range(len(models)):
    #     for j in range(len(arabic_sentences)):
    #         print(
    #             f"Model: {models[i]}, Sentence: {arabic_sentences[j]}, Target: {targets.loc[j, model_name]}, Success Level: {benchList.loc[j, model_name]}"
    #         )

    return benchList, targets




# run following if this file is run directly
if __name__ == "__main__":
    # 6 models
    models = [
        "awwab-ahmed/bert-base-arabic-camelbert-msa-sixteenth-finetuned-AR-dotted-mediumPlus",
        "CAMeL-Lab/bert-base-arabic-camelbert-mix",
        "UBC-NLP/ARBERT",
        "UBC-NLP/MARBERT",
        "UBC-NLP/MARBERTv2",
        "aubmindlab/bert-large-arabertv2",
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
        "أنا أعمل في شركة كبيرة",
        "أختي تلعب مع أصدقائها",
        "أشاهد التلفاز في المساء",
        "نحن نذهب إلى السوق يوم السبت",
        "عندي دراجة جديدة",
        "أبي يقرأ الجريدة كل صباح",
        "نحن نأكل العشاء في المطعم",
        "الطائرة تقلع من المطار الآن",
        "أدرس الرياضيات كل يوم",
        "أحب السفر إلى دول جديدة",
        "أعمل على مشروع جديد",
        "السيارة تقف أمام البيت",
        "السماء مليئة بالنجوم الليلة",
        "أحب الذهاب إلى الشاطئ في الصيف",
        "جدي يحب الزراعة في الحديقة",
        "أذهب إلى المكتبة لقراءة الكتب",
        "أبي يعمل في مكتب حكومي",
        "المدرسة تبدأ الساعة الثامنة صباحا",
        "أختي تحب الرسم في وقت فراغها",
        "أشتري الخضروات من السوق",
        "نحن نستمتع بالتنزه في الحديقة"
    ]

    benchList, targets = benchmark(models, arabic_sentences)