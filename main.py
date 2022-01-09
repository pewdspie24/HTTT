import json
from underthesea import word_tokenize as vn_token_uts
from underthesea import pos_tag
import pandas
from googletrans import Translator
translator = Translator()

WTYPE_MATCH = {'danhtuchung':'noun', 'dongtu':'verb', 'tinhtu':'adj', 'sotu':'number', 'luongtu':'adj', 'photu':'advA', 'photuchimucdo':'advB', 'photuthoigian':'advB', 'daitu':'pronoun', 'thantu':'excl', 'quanhetulietke':'conj', 'quanhetudinhvi':'prep', 'chitu':'det', 'daituxungho':'pronoun'}
TENSE = ['present', 'past', 'future', 'continous']
FLAG = 0
PATH_VI = ["chitu.txt", "daituchi_hd.txt", "daituxungho.txt", "danhtuchiloai.txt", "danhtuchung.txt", "danhtudonvi.txt", 
        "dongtu.txt", "luongtu.txt", "photuchimucdo.txt", "photuphudinh.txt", "photuthoigian.txt", 
        "quanhetudinhvi.txt", "quanhetulietke.txt", "sotu.txt", "thantu.txt", "tinhtu.txt"]
VI_DICT_PATH = "viet_dict/dict_chitiet/"
word_type_vi = {}

def get_token(text):
    final = ""
    for word in text:
        final += word
        final += " "
    return final

def get_word_type_vi(tokens):
    I_flag = False
    word = []
    type_word = []
    thi = "present"
    main_verb = 0 
    for token in tokens:
        try:
            type_word.append(word_type_vi[token])
            word.append(token)
            # print("co trong dict")
            # print(word)
        except :
            if token in ",":
                word.append(token)
                type_word.append('lietke')
                # print("là dấu câu")
                # print(word)
            elif "A" <= token[0] and token[0] <= "Z":
                word.append(token)
                type_word.append("daituxungho")
                # print("là tên riêng")
                # print(word)
            else:
                word.append(token)
                type_word.append("")
                if len(word) == 0:
                    type_word.append("danhtuchung")
                
                # print("từ vô định")
                # print(word)
    num = len(word)
    # print("Word o day:"+str(num))
    # print(type_word)
    for idx in range(num) :
        word_type = type_word[idx].split(" ")
        # print(idx, ". ",word[idx], ": ", type_word[idx])
        # decide thi 
        if word[idx] in ["đã", "mới", "vừa", "từng"]:
            thi = "past"
        elif word[idx] == "đang":
            thi = "continous"
        elif word[idx] in ["sẽ", "sắp", "sắp sửa"]:
            thi = "future"  
        # convert danhtuchiloai to noun
        if type_word[idx] == "danhtuchiloai": 
            if idx+1 == num or (idx+1 < num and type_word[idx+1] not in ["danhtuchung", "danhtuchiloai"]):
                type_word[idx] = "danhtuchung"
        # in case multiple word type
        if len(word_type) > 1:
            if idx >= 1:
                # decide 
                if type_word[idx-1] in ["lietke", "quanhetulietke"]:
                    type_word[idx] = type_word[idx-2]
                # decide photuchimucdo
                elif "photuchimucdo" in type_word[idx]:
                    if type_word[idx-1] in ["dongtu", "tinhtu"]:
                        type_word[idx] = "photuchimucdo"
                # decide noun
                elif type_word[idx-1] == "danhtuchiloai":
                    type_word[idx] = "danhtuchung"
                # decide verb
                elif type_word[idx-1] == "photuthoigian":
                    type_word[idx] = "dongtu"
                
                elif type_word[idx-1] == "photuchimucdo":
                    if "dongtu" in type_word[idx]:
                        type_word[idx] = "dongtu"
                    elif "tinhtu" in type_word[idx]:
                        type_word[idx] = "tinhtu"
                # decide adj
                elif type_word[idx-1] in ["danhtuchung", "dongtu", "photuchimucdo"]:
                    type_word[idx] = "tinhtu"    
                        
            elif idx+1 < num:
                # decide 
                if type_word[idx+1] in ["lietke", "quanhetulietke"]:
                    type_word[idx] = type_word[idx+2]
                # decide noun
                elif type_word[idx+1] != "danhtuchung":
                    type_word[idx] = "danhtuchung"
                elif type_word[idx+1] == "chitu":
                    type_word[idx] = "danhtuchung"
                # decide verb
                elif type_word[idx+1] == "photuchimucdo":
                    if "dongtu" in type_word[idx]:
                        type_word[idx] = "dongtu"
                    elif "tinhtu" in type_word[idx]:
                        type_word[idx] = "tinhtu"
        # print(word_type)
                        
    for idx, type_word1 in enumerate(type_word) :
        if type_word1 in ["danhtuchiloai", "photuthoigian"]:
            word.pop(idx)
            type_word.pop(idx)
    for idx, type_word1 in enumerate(type_word) :
        if type_word1 == "dongtu":
            main_verb = idx
            break
    if main_verb == 0:
        for idx, type_word1 in enumerate(type_word) :
            if type_word1 == "tinhtu":
                main_verb = idx
                break
    return word, type_word, thi, main_verb

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
    for i in PATH_VI:
        with open(VI_DICT_PATH + i, "r+", encoding="utf-8" ) as f:
            for line in f.readlines():
                tmp = line.strip()
                if tmp in word_type_vi:
                    word_type_vi[tmp] += " " + i[:-4]
                else:
                    word_type_vi[tmp] = i[:-4]    
    # Process
    # print(pronoun[0])
    # for j in pronoun[1].values():
    #     print(j[0])
    while True:
        PRONOUN = 0
        NEG = 0
        # 1. Input text
        sequence = "tôi là một học sinh"
        # 2. Tokenize text
        tokens = vn_token_uts(sequence)
        # 3.1 Get VI type, primary Verb, Tense
        word_list_vi, word_type_vi, tense, primary_idx = get_word_type_vi(tokens)
        for idx, word in enumerate(word_list_vi):
            print(word+" "+word_type_vi[idx])
        # print(primary_idx)
        # 3.2 Get C-V
        # primary_idx += 1
        NEG = get_neg(tokens)
        # 4.1 Matching word
        vi_sentence = []
        # vi_sentence = ((tu1,(loaitu1, 1)), (tu2,(loaitu2, 2)), ...)
        for idx, token in enumerate(word_list_vi):
            vi_sentence.append((token,(word_type_vi[idx], idx)))
        eng_sentence = []
        # eng_sentence = ((tu1,(loaitu1, 1)), (tu2,(loaitu2, 2)), ...)
        idx = 0
        for word in vi_sentence:
            k, v = word[0], word[1]
            # print("ATT",v[0])
            if v[0] == 'lietke':
                c = []
                c.append(k)
                eng_sentence.append((c,('lietke', idx)))
                continue
            if v[0] == 'daituxungho' and k[0].isupper():
                c = []
                c.append(k)
                # print(c)
                eng_sentence.append((c,('proper', idx)))
                continue
            flag = 0
            idx+=1
            for idx_en, i in enumerate(vi_eng_dict):
                if k == i['word']:
                    vi_type = v[0]
                    print(vi_type)
                    # Exist in matching-type
                    if vi_type in WTYPE_MATCH:
                        print(WTYPE_MATCH.get(vi_type))
                        # Exist in dictionary with type
                        # print(i['type'])
                        if 'type' in i and WTYPE_MATCH.get(vi_type) in i['type']: 
                            # print("cc")
                            trans_idx = 0
                            res = {}
                            name_trans = ""
                            for type in i['type']:
                                if 'trans'+str(trans_idx) in i:
                                    res.update(type=i['trans'+str(trans_idx)])
                                    if type == WTYPE_MATCH.get(vi_type):
                                        name_trans = 'trans'+str(trans_idx)
                                else:
                                    trans_idx+=1
                                    res.update(type=i['trans'+str(trans_idx)])
                                    if type == WTYPE_MATCH.get(vi_type):
                                        name_trans = 'trans'+str(trans_idx)
                                trans_idx+=1
                            # print(i[name_trans])
                            list_words = i[name_trans]
                            print(list_words)
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
        # print(vi_sentence)
        for i in range(0, primary_idx):
            type_vi = vi_sentence[i][1][0]
            type_en = eng_sentence[i][1][0]
            word_en = eng_sentence[i][0][0]
            print("")
            print(vi_sentence[i][1][0])
            print(eng_sentence[i][1][0])
            print(eng_sentence[i][0][0])
            # If include conj, becomes plural
            if type_vi == 'quanhetulietke':
                PRONOUN = 1
                break
            # If proper, becomes singular
            if type_en == 'proper':
                continue
            # Decide pronoun in database
            if type_en == 'pronoun':
                if word_en == "I":
                    I_flag = True
                for j in pronoun[1].values():
                    for smt in j:
                        if word_en == smt:
                            PRONOUN = 1
                            print("CC")
                            break
                    if PRONOUN:
                        break # TODO
                if PRONOUN:
                    break
            # If uncountable noun, becomes singular
            if word_en in uncount_noun:
                continue
            # print(word_en)
            # If plural noun
            if word_en in plural:
                PRONOUN = 1
                break       
        verb = eng_sentence[primary_idx][0][0]
        v_type = eng_sentence[primary_idx][1][0]
        # print(eng_sentence)
        # print("ditmemay", primary_idx)
        # print(verb)
        # print(v_type)
        # Verb is verb
        if v_type == 'verb' and verb != "be":
            if tense == 'present':
                if PRONOUN == 0 or I_flag:
                    if NEG == 0:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0][0] = v[1]
                                break
                    else:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0][0] = "does not "+v[0]
                                break
                else:
                    if NEG == 0:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0][0] = v[0]
                                break
                    else:
                        for v in verbs:
                            if v[0] == verb:
                                eng_sentence[primary_idx][0][0] = "do not "+v[0]
                                break
            elif tense == 'past':
                for v in verbs:
                    if v[0] == verb:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = v[2]
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "did not "+v[0]
                            break
            elif tense == 'future':
                for v in verbs:
                    if v[0] == verb:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = 'will '+v[0]
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = 'will not '+v[0]
                            break
            elif tense == 'continous':
                if PRONOUN == 0:
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0][0] = "is "+v[4]
                                break
                            else:
                                eng_sentence[primary_idx][0][0] = "is not "+v[4]
                                break
                elif I_flag == False:
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0][0] = "are "+v[4]
                                break
                            else:
                                eng_sentence[primary_idx][0][0] = "are not "+v[4]
                                break
                else:
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0][0] = "am "+v[4]
                                break
                            else:
                                eng_sentence[primary_idx][0][0] = "am not "+v[4]
                                break
        # other cases
        elif verb != "be":
            if PRONOUN == 0:
                if tense == 'present':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = "is "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "is not "+verb
                            break
                    elif I_flag == False:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = "are "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "are not "+verb
                            break
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = "am "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "am not "+verb
                            break
                elif tense == 'past':
                    if NEG == 0:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0][0] = "was "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "were "+verb
                            break
                    else:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0][0] = "was not "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "were not "+verb
                            break
                elif tense == 'future':
                    for v in verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0][0] = 'will be '+verb
                                break
                            else:
                                eng_sentence[primary_idx][0][0] = 'will not be '+verb
                                break
                elif tense == 'continous':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = "is "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "is not "+verb
                            break
                    elif I_flag == False:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = "are "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "are not "+verb
                            break
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = "am "+verb
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = "am not "+verb
                            break
        else:
            if tense == 'present':
                if PRONOUN == 0:
                    if NEG == 0:
                        eng_sentence[primary_idx][0][0] = "is"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "is not"
                        break
                elif I_flag == False:
                    if NEG == 0:
                        eng_sentence[primary_idx][0][0] = "are"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "are not"
                        break
                else:
                    if NEG == 0:
                        eng_sentence[primary_idx][0][0] = "am"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "am not"
                        break
            elif tense == 'past':
                if NEG == 0:
                    if PRONOUN == 0:
                        eng_sentence[primary_idx][0][0] = "was"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "were"
                        break
                else:
                    if PRONOUN == 0:
                        eng_sentence[primary_idx][0][0] = "was not"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "were not"
                        break
            elif tense == 'future':
                for v in verbs:
                    if v[0] == verb:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = 'will be'
                            break
                        else:
                            eng_sentence[primary_idx][0][0] = 'will not be'
                            break
            elif tense == 'continous':
                if PRONOUN == 0:
                    if NEG == 0:
                        eng_sentence[primary_idx][0][0] = "is"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "is not"
                        break
                elif I_flag == False:
                    if NEG == 0:
                        eng_sentence[primary_idx][0][0] = "are"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "are not"
                        break
                else:
                    if NEG == 0:
                        eng_sentence[primary_idx][0][0] = "am"
                        break
                    else:
                        eng_sentence[primary_idx][0][0] = "am not"
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
        for i in eng_sentence:
            if i[1][1] != None:
                print(i[0], end=" ")
        print("")
        for i in eng_sentence:
            if i[1][1] != None:
                print(i[0][0], end=" ")
        break
        

    # sentence = "mọi người đều thích điều này"
    # abc = get_token(sentence)
    # print(abc)
