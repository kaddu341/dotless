from pyARdotless import *


model_name = "CAMeL-Lab/bert-base-arabic-camelbert-mix"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForMaskedLM.from_pretrained(model_name)
ArListem = ArabicLightStemmer()


test_string = 'أهلا أنا إسمي عمار'
index = 1

single_test(tokenizer, model, ArListem, specific_string=test_string, specific_index=index, gen_prob_func=get_candidate_word_probabilities)


