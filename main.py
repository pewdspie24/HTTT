import json
from underthesea import word_tokenize as vn_token_uts
from underthesea import pos_tag
import pandas
from googletrans import Translator
translator = Translator()

WTYPE_MATCH = {'Danhtu':'noun', 'Dongtu':'verb', 'Tinhtu':'adj', 'Sotu':'adj', 'Sotu':'number', 'Luongtu':'adj', 'Photu':'advA', 'Photuchimucdo':'advB', 'Photuthoigian':'advB', 'Daitu':'pronoun', 'Thantu':'excl', 'Quanhetulietke':'conj', 'Quanhetudinhvi':'prep', 'Chitu':'det'}
TENSE = ['present', 'past', 'future', 'continous']
FLAG = 0

def get_nth_value(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, values in enumerate(dictionary.values()):
        if i == n:
            return values
    raise IndexError("dictionary index out of range") 

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, keys in enumerate(dictionary.keys()):
        if i == n:
            return keys
    raise IndexError("dictionary index out of range") 

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

def get_tense(tokens):
    idx = 0
    return TENSE[idx]

def get_neg(tokens):
    NEG = 0
    return NEG

def get_from_JSON(text, list):
    # if text == 
    return 0

if __name__ == "__main__":
    # English loading, list of dict
    with open("eng_dict\data.json", 'r', encoding="utf8") as j:
        vi_eng_dict = json.loads(j.read())
    with open("eng_dict\pronouns.json", 'r', encoding="utf8") as j:
        pronoun = json.loads(j.read())
    with open("eng_dict\\verb.json", 'r', encoding="utf8") as j:
        verbs = json.loads(j.read())
    with open("eng_dict\words_dictionary.json", 'r', encoding="utf8") as j:
        eng_dict = json.loads(j.read())
    with open("eng_dict\\uncountable_noun.txt", 'r', encoding="utf8") as j:
        uncount_noun = j.read().splitlines() 
        
    nouns = pandas.read_csv("eng_dict\\noun.csv")
    plural = nouns['plural']
    singular = nouns['singular']
    # Vietnamese loading
        
    # Process
    # print(singular[999], plural[999])
    
    while True:
        PRONOUN = 0
        NEG = 0
        # 1. Input text
        sequence = input()
        # 2. Tokenize text
        tokens = vn_token_uts(sequence)
        # 3.1 Get VI type
        word_type_vi = get_word_type_vi(tokens)
        # 3.2 Get C-V
        primary_idx = get_CV(tokens)
        NEG = get_neg(tokens)
        # 3.3 Determine tense
        tense = get_tense(tokens)
        # 4.1 Matching word
        vi_sentence = []
        # vi_sentence = ((tu1,(loaitu1, 1)), (tu2,(loaitu2, 2)), ...)
        for idx, token in enumerate(tokens):
            vi_sentence.append((token,(word_type_vi[idx], idx)))
        eng_sentence = []
        # eng_sentence = ((tu1,(loaitu1, 1)), (tu2,(loaitu2, 2)), ...)
        idx = 0
        for word in vi_sentence:
            k, v = word[0], word[1]
            if k[0].isupper():
                eng_sentence.append((k,('proper', idx)))
                continue
            flag = 0
            idx+=1
            for idx_en, i in enumerate(vi_eng_dict):
                if k == i['word']:
                    vi_type = v[0]
                    # Exist in matching-type
                    if vi_type in WTYPE_MATCH:
                        # Exist in dictionary with type
                        if vi_type in i['type']: 
                            trans_idx = 0
                            res = {}
                            for type in i['type']:
                                if 'trans'+str(trans_idx) in i:
                                    res.update(type=i['trans'+str(trans_idx)])
                                else:
                                    trans_idx+=1
                                    res.update(type=i['trans'+str(trans_idx)])
                                trans_idx+=1
                            list_words = i[res.get(type)]
                            eng_sentence.append((list_words,(WTYPE_MATCH.get(vi_type), idx)))
                            flag = 1
                        # Don't exist in dictionary with type
                        else:
                            list_words = []
                            for key in i.keys():
                                if key[0:3] == 'tra':
                                    for obj in i.get(key):
                                        list_words.append(obj)
                            eng_sentence.append((list_words,(WTYPE_MATCH.get(vi_type), idx)))
                            flag = 2
                    # Don't existed in matching-type
                    else:
                        list_words = []
                        for key in i.keys():
                            if key[0:3] == 'tra':
                                for obj in i.get(key):
                                    list_words.append(obj)
                        eng_sentence.append((list_words,(None, idx)))
                        flag = 3
            # Can't find in dict
            if flag == 0:
                eng_sentence.append((k,(None, idx)))
                
        # 4.2 Correct the elements
        # Define type of subject
        for i in range(0, primary_idx):
            type_vi = vi_sentence[i][1][0]
            type_en = eng_sentence[i][1][0]
            word_en = eng_sentence[i][0]
            if type_vi == 'Quanhetulietke':
                PRONOUN = 1
                break
            if type_en == 'proper':
                break
            if type_en == 'pronoun':
                for j in pronoun[1].values():
                    if word_en == j:
                        PRONOUN = 1
                        break
                break # TODO
            if word_en in uncount_noun:
                break
            if word_en in plural:
                PRONOUN = 1
                break
        verb = eng_sentence[primary_idx][0]
        v_type = eng_sentence[primary_idx][1][0]
        # Verb is verb
        if v_type == 'verb' and verb != "be":
            if tense == 'present':
                if PRONOUN == 0:
                    if NEG == 0:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0] = v[1]
                                break
                    else:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0] = "is not "+v[0]
                                break
                else:
                    if NEG == 0:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0] = v[0]
                                break
                    else:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0] = "are not "+v[0]
                                break
            elif tense == 'past':
                for v in verbs:
                    if v[0] == verb:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = v[2]
                            break
                        else:
                            eng_sentence[primary_idx][0] = "did not "+v[0]
                            break
            elif tense == 'future':
                for v in verbs:
                    if v[0] == verb:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = 'will '+v[0]
                            break
                        else:
                            eng_sentence[primary_idx][0] = 'will not '+v[0]
                            break
            elif tense == 'continous':
                if PRONOUN == 0:
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0] = "is "+v[4]
                                break
                            else:
                                eng_sentence[primary_idx][0] = "is not "+v[4]
                                break
                else:
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0] = "are "+v[4]
                                break
                            else:
                                eng_sentence[primary_idx][0] = "are not "+v[4]
                                break
        # other cases
        elif verb != "be":
            if PRONOUN == 0:
                if tense == 'present':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "is "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0] = "is not "+verb
                            break
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "are "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0] = "are not "+verb
                            break
                elif tense == 'past':
                    if NEG == 0:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0] = "was "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0] = "were "+verb
                            break
                    else:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0] = "was not "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0] = "were not "+verb
                            break
                elif tense == 'future':
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0] = 'will be '+verb
                                break
                            else:
                                eng_sentence[primary_idx][0] = 'will not be '+verb
                                break
                elif tense == 'continous':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "is "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0] = "is not "+verb
                            break
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "are "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0] = "are not "+verb
                            break
        else:
            if PRONOUN == 0:
                if tense == 'present':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "is"
                            break
                        else:
                            eng_sentence[primary_idx][0] = "is not"
                            break
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "are"
                            break
                        else:
                            eng_sentence[primary_idx][0] = "are not"
                            break
                elif tense == 'past':
                    if NEG == 0:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0] = "was"
                            break
                        else:
                            eng_sentence[primary_idx][0] = "were"
                            break
                    else:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0] = "was not"
                            break
                        else:
                            eng_sentence[primary_idx][0] = "were not"
                            break
                elif tense == 'future':
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0] = 'will be'
                                break
                            else:
                                eng_sentence[primary_idx][0] = 'will not be'
                                break
                elif tense == 'continous':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "is"
                            break
                        else:
                            eng_sentence[primary_idx][0] = "is not"
                            break
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0] = "are"
                            break
                        else:
                            eng_sentence[primary_idx][0] = "are not"
                            break
        # 5. Re-organize sentence
        for word in eng_sentence:
            # Adjective comes before nouns
            if word[1][0] == 'adj':
                adj_idx_en = word[1][1]
                adj_idx_vi = adj_idx_en
                for i in range (adj_idx_en, 0, -1):
                    if eng_sentence[i][1][0] == 'noun':
                        eng_sentence[i][0] = word[0] + " " + eng_sentence[i][0]
                        word[0] = ""
                        word[1][0] = None
            # Adverbs Before comes before nouns
            if word[1][0] == 'advB':
                adv_idx_en = word[1][1]
                adv_idx_vi = adv_idx_en
                for i in range (adv_idx_en, len(eng_sentence)):
                    if eng_sentence[i][1][0] == 'noun' or eng_sentence[i][1][0] == 'verb' or eng_sentence[i][1][0] == 'adj':
                        eng_sentence[i][0] = word[0] + " " + eng_sentence[i][0]
                        word[0] = ""
                        word[1][0] = None
            # Adverbs After comes after nouns
            if word[1][0] == 'advA':
                adv_idx_en = word[1][1]
                adv_idx_vi = adv_idx_en
                for i in range (adv_idx_en, 0, -1):
                    if eng_sentence[i][1][0] == 'noun' or eng_sentence[i][1][0] == 'verb' or eng_sentence[i][1][0] == 'adj':
                        eng_sentence[i][0] =  eng_sentence[i][0] + " " + word[0]
                        word[0] = ""
                        word[1][0] = None
            # Deteminers comes before nouns
            if word[1][0] == 'det':
                det_idx_en = word[1][1]
                det_idx_vi = det_idx_en
                for i in range (det_idx_en, 0, -1):
                    if eng_sentence[i][1][0] == 'noun' :
                        eng_sentence[i][0] =  word[0] + " " + eng_sentence[i][0] 
                        word[0] = ""
                        word[1][0] = None
            
        # 6. Show result & Suggest 
        


    # sentence = "mọi người đều thích điều này"
    # abc = get_token(sentence)
    # print(abc)
