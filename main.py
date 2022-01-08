import json
from underthesea import word_tokenize as vn_token_uts
from underthesea import pos_tag
import pandas
from googletrans import Translator
translator = Translator()

WTYPE_MATCH = {'Danhtu':'noun', 'Dongtu':'verb', 'Tinhtu':'adj', 'Sotu':'adj', 'Sotu':'number', 'Luongtu':'adj', 'Photu':'adv', 'Daitu':'pronoun', 'Thantu':'excl', 'Quanhetu':'conj', 'Gioitu':'prep'}

def get_token(text):
    final = ""
    for word in text:
        final += word
        final += " "
    return final

def get_word_type_vi(tokens):
    word_type_vi = []
    # TODO: Code for searching type, using POS Tagging for improving accuracy

def get_CV(tokens):
    idx = 0
    # TODO: Return index of primary verb
    return idx

def get_from_JSON(text, list):
    # if text == 
    return 0

if __name__ == "__main__":
    # English loading
    with open("eng_dict\data.json", 'r', encoding="utf8") as j:
        vi_eng_dict = json.loads(j.read())
    with open("eng_dict\pronouns.json", 'r', encoding="utf8") as j:
        pronoun = json.loads(j.read())
    with open("eng_dict\singular_noun.json", 'r', encoding="utf8") as j:
        singular_noun = json.loads(j.read())
    with open("eng_dict\\verb.json", 'r', encoding="utf8") as j:
        verbs = json.loads(j.read())
    with open("eng_dict\words_dictionary.json", 'r', encoding="utf8") as j:
        eng_dict = json.loads(j.read())
    nouns = pandas.read_csv("eng_dict\\noun.csv")
    plural = nouns['plural']
    singular = nouns['singular']

    # Vietnamese loading
        
    # Process
    # print(singular[999], plural[999])
    
    while True:
        # 1. Input text
        sequence = input()
        # 2. Tokenize text
        tokens = vn_token_uts(sequence)
        # 3.1 Get VI type
        word_type_vi = get_word_type_vi(tokens)
        # 3.2 Get C-V
        primary_idx = get_CV(tokens)
        # 3.3 Determine tense
        # 4. Matching word
        # 5. Re-organize sentence
        # 6. Show result & Suggest 
        


    # sentence = "mọi người đều thích điều này"
    # abc = get_token(sentence)
    # print(abc)
