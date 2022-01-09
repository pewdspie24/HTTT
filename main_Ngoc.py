import json
from underthesea import word_tokenize as vn_token_uts
from underthesea import pos_tag
import pandas
from googletrans import Translator
translator = Translator()

link_add = "viet_dict/dict_chitiet/"
word_type_vi = {}
path = ["chitu.txt", "daituchi_hd.txt", "daituxungho.txt", "danhtuchiloai.txt", "danhtuchung.txt", "danhtudonvi.txt", 
        "dongtu.txt", "luongtu.txt", "photuchimucdo.txt", "photuphudinh.txt", "photuthoigian.txt", 
        "quanhetudinhvi.txt", "quanhetulietke.txt", "sotu.txt", "thantu.txt", "tinhtu.txt"]

WTYPE_MATCH = {'Danhtu':'noun', 'Dongtu':'verb', 'Tinhtu':'adj', 'Sotu':'adj', 'Sotu':'number', 'Luongtu':'adj', 'Photu':'adv', 'Daitu':'pronoun', 'Thantu':'excl', 'Quanhetu':'conj', 'Gioitu':'prep'}

def get_token(text):
    final = ""
    for word in text:
        final += word
        final += " "
    return final

def get_word_type_vi(tokens):
    word = []
    type_word = []
    thi = "HTD"
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
    print(word)
    print(type_word)
    for idx in range(num) :
        word_type = type_word[idx].split(" ")
        print(idx, ". ",word[idx], ": ", type_word[idx])
        # decide thi 
        if word[idx] in ["đã", "mới", "vừa", "từng"]:
            thi = "QK"
        elif word[idx] == "đang":
            thi = "HTTD"
        elif word[idx] in ["sẽ", "sắp", "sắp sửa"]:
            thi = "TLD"  
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
                # decide verd
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
                # decide verd
                elif type_word[idx+1] == "photuchimucdo":
                    if "dongtu" in type_word[idx]:
                        type_word[idx] = "dongtu"
                    elif "tinhtu" in type_word[idx]:
                        type_word[idx] = "tinhtu"
                        
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
    for i in path:
        with open(link_add + i, "r+", encoding="utf-8" ) as f:
            for line in f.readlines():
                tmp = line.strip()
                if tmp in word_type_vi:
                    word_type_vi[tmp] += " " + i[:-4]
                else:
                    word_type_vi[tmp] = i[:-4]
    
    # Process
    # print(singular[999], plural[999])
    
    while True:
        # 1. Input text
        sequence = input()
        # 2. Tokenize text
        tokens = vn_token_uts(sequence)
        # 3.1 Get VI type
        word, type_word, thi, main_verb = get_word_type_vi(tokens)
        # 3.2 Get C-V
        # primary_idx = get_CV(tokens)
        # 3.3 Determine tense
        # 4. Matching word
        # 5. Re-organize sentence
        # 6. Show result & Suggest 
        
        # sentence = "tôi, Ngọc và bạn cùng ăn, chơi với nhau"
        # abc = vn_token_uts(sentence)
        print(word)
        print(type_word)
        print(thi)
        print(main_verb)

# sentence = "tôi, Ngọc và bạn cùng ăn, chơi với nhau"
# abc = vn_token_uts(sentence)
# print(abc)



                    