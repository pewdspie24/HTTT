import sys
import json
import re
from typing import Sequence
from underthesea import word_tokenize as vn_token_uts
from underthesea import pos_tag
import pandas
import numpy as np
from googletrans import Translator
translator = Translator()

WTYPE_MATCH = {'danhtuchung':'noun', 'dongtu':'verb', 'tinhtu':'adj', 'sotu':'number', 'luongtu':'adj', 'photu':'advA', 'photuchimucdo':'advB', 'photuthoigian':'advB', 'daitu':'pronoun', 'thantu':'excl', 'quanhetulietke':'conj', 'quanhetudinhvi':'prep', 'chitu':'det', 'daituxungho':'pronoun'}
TENSE = ['present', 'past', 'future', 'continous']
FLAG = 0
PATH_VI = ["chitu.txt", "daituxungho.txt", "danhtuchiloai.txt", "danhtuchung.txt",  
        "dongtu.txt", "luongtu.txt", "photuchimucdo.txt", "photuphudinh.txt", "photuthoigian.txt", 
        "quanhetudinhvi.txt", "quanhetulietke.txt", "sotu.txt", "thantu.txt", "tinhtu.txt"]
VI_DICT_PATH = "viet_dict/dict_chitiet/"
TO_VERB = ["hate", "hope", "intend", "like", "love", "mean", "plan", "try", "want", 'go']
POSSESIVE = {'I':'my', 'you':'your', 'he':'his', 'she':'her', 'it':'its', 'we':'our', 'they':'their'}
POSSESIVE_LIST = ['my', 'your', 'his', 'her', 'its', 'our', 'their']

class MainProcess():
    def __init__(self):   
        self.word_type_vi = {}
         # English loading, list of dict
        with open("eng_dict\data.json", 'r', encoding="utf8") as j:
            self.vi_eng_dict = json.loads(j.read())
        with open("eng_dict\pronouns.json", 'r', encoding="utf8") as j:
            self.pronoun = json.loads(j.read())
        with open("eng_dict\\verb.json", 'r', encoding="utf8") as j:
            self.verbs = json.loads(j.read())
        with open("eng_dict\words_dictionary.json", 'r', encoding="utf8") as j:
            self.eng_dict = json.loads(j.read())
        with open("eng_dict\\uncountable_noun.txt", 'r', encoding="utf8") as j:
            self.uncount_noun = j.read().splitlines() 
            
        nouns = pandas.read_csv("eng_dict\\noun.csv")
        self.plural = nouns.plural.to_list()
        self.singular = nouns.singular.to_list()
        # Vietnamese loading
        for i in PATH_VI:
            with open(VI_DICT_PATH + i, "r+", encoding="utf-8" ) as f:
                for line in f.readlines():
                    tmp = line.strip()
                    if tmp in self.word_type_vi:
                        self.word_type_vi[tmp] += " " + i[:-4]
                    else:
                        self.word_type_vi[tmp] = i[:-4]    

    # Chuyển tên riêng từ tiếng việt sang anh
    def no_accent_vietnamese(self, s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s

    def check_number(self, word):
        tmp = word
        if "," in tmp:
            tmp = tmp.replace(",","")
        try:
            float(tmp)
            return True
        except:
            return False

    def get_word_type_vi(self, tokens):
        word = []
        type_word = []
        thi = "present"
        main_verb = 0
        neg = 0
        check =True
        for token in tokens:
            try: # if Vi word exist in Vi dict
                type_word.append(self.word_type_vi[token])
                word.append(token)
            except :
                # if is ",", may be consider as quanhetulietke
                if token in ",":
                    word.append(token)
                    type_word.append("lietke")
                # if is special character
                elif token in "-:%'(){}[]":
                    word.append(token)
                    type_word.append("kytu")
                # if the first character is uppper, consider as a name
                elif "A" <= token[0] and token[0] <= "Z":
                    word.append(token)
                    type_word.append("daituxungho")
                # if is number
                # elif self.check_number(self, token) == True:
                #     word.append(token)
                #     type_word.append("so")
                # if is the first word, consider as a noun
                elif len(word) == 0:
                    word.append(token)
                    type_word.append("danhtuchung")
                else: 
                    word.append(token)
                    type_word.append("unknown")

        num = len(word)
        print(word)          
        print(type_word)
        while (check): # if check == True, it mean, still having changes
            tmp = type_word.copy()  
            for idx in range(num) :
                word_type = type_word[idx].strip().split(" ")
                # determine tense 
                if word[idx] in ["đã", "từng", "hôm qua", "hôm xưa", "ngày xưa"]:
                    thi = "past"
                elif word[idx] in ["đang", "hôm nay"]:
                    thi = "continous"
                elif word[idx] in ["sẽ", "ngày kìa", "ngày mai"]:
                    thi = "future"  
                #determine danhtuchiloai or verb: bó, cuốn, tập, ...
                if "danhtuchiloai dongtu" in type_word[idx]:
                    # if before word is sotu or luong tu
                    if idx-1>0 and type_word[idx-1] in ["sotu", "luongtu", "dongtu", "quanhetudinhvi"]:
                        type_word[idx] = "danhtuchiloai"
                    else:
                        type_word[idx] = "dongtu"
                # convert danhtuchiloai to noun
                if "danhtuchiloai" in type_word[idx] and (idx+1 == num or (idx+1 < num and "danhtu" not in type_word[idx+1])): 
                        type_word[idx] = "danhtuchung"
                # determine noun or sotu
                if word[idx] == "ba":
                    if (idx>0 and "danhtuchung" in type_word[idx-1])or (idx+1<num and "danhtu" in type_word[idx+1]):
                        type_word[idx] = "sotu"
                    else:
                        type_word[idx] = "danhtuchung"
                #determine quanhetudinhvi or verb or noun
                if "quanhetudinhvi" in type_word[idx]:
                    # if idx+1 <num and np.any([i in type_word[idx+1] for i in ["danhtu", "sotu", "luongtu", "daituxungho", "so"]]):
                    if idx>1 and np.any([i in type_word[idx-1] for i in ["dongtu", "tinhtu"]]):
                        type_word[idx] = "quanhetudinhvi"
                    else:
                        type_word[idx] = type_word[idx].replace("quanhetudinhvi","")    
                # in case multiple word type
                if len(word_type) > 1:
                    if idx >= 1: # base on before word
                        # determine type of word basing on "," or quanhetulietke
                        if type_word[idx-1] in ["lietke", "quanhetulietke"]:
                            type_word[idx] = type_word[idx-2]
                        # determine noun
                        elif "danhtuchung" in type_word[idx]:
                            if np.any([i in type_word[idx-1] for i in ["sotu", "luongtu", "danhtuchiloai", "quanhetudinhvi"]]) or word[idx-1] == "của":
                                type_word[idx] = "danhtuchung"
                            elif np.any([i in type_word[idx-1] for i in ["daituxungho", "danhtuchung"]]):
                                type_word[idx] = type_word[idx].replace("danhtuchung","")
                        # determine verb or adj, priority verb first
                        elif np.any([i in type_word[idx-1] for i in ["danhtuchung", "photu", "daituxungho"]]):
                            if "dongtu" in type_word[idx]:
                                type_word[idx] = "dongtu"
                            elif "tinhtu" in type_word[idx]:
                                type_word[idx] = "tinhtu"  
                        elif "tinhtu" in type_word[idx] and "dongtu" in type_word[idx-1]:
                            type_word[idx] = "tinhtu" 
                    elif idx+1 < num:
                        # determine type of word basing on "," or quanhetulietke 
                        if type_word[idx+1] in ["lietke", "quanhetulietke"]:
                            type_word[idx] = type_word[idx+2]
                        # determine noun
                        elif "danhtuchung" in type_word[idx] and np.any(i in type_word[idx+1] for i in ["chitu", "dongtu", "tinhtu", "photu"]) :
                            type_word[idx] = "danhtuchung"
                        # determine verb
                        elif "dongtu" in type_word[idx] and np.any(i in type_word[idx+1] for i in ["photuchimucdo", "quanhetudinhvi", "sotu", "luongtu", "danhtu", "tinhtu"]):
                            type_word[idx] = "dongtu"
                        # determine verb or adj
                        elif "tinhtu" in type_word[idx] and type_word[idx+1] == "photuchimucdo":
                            type_word[idx] = "tinhtu"
            check = not np.array_equal(tmp, type_word)
            print("lap")
        # delete unneed word  
        dem = 0              
        while dem<num:
            print(word)          
            print(type_word) 
            print(dem, " ", num, " ", type_word[dem], " ", word[dem])
            if (dem+1<num and np.any([i in type_word[dem+1] for i in ["dongtu", "tinhtu"]])):
                if "photuphudinh" in type_word[dem] or word[dem] in ["đã", "từng", "đang", "sẽ"]:
                    main_verb = dem  
                # elif "photuchimucdo" in type_word[dem]:
                #     main_verb = dem + 1
            if type_word[dem] in ["danhtuchiloai", "photuphudinh"] or word[dem] in ["đã", "từng", "đang", "sẽ"]:
                if "photuphudinh" in type_word[dem]:
                    neg = 1
                word.pop(dem)
                type_word.pop(dem)
                num = num-1
            else:
                dem +=1
        # find main verb
        if main_verb == 0:
            for idx, type_word1 in enumerate(type_word) :
                if type_word1 == "dongtu":
                    main_verb = idx
                    break
        if main_verb == 0:
            for idx, type_word1 in enumerate(type_word) :
                if type_word1 == "tinhtu":
                    main_verb = idx
                    break
        
        print(thi, " ", main_verb, " ", neg)
        return word, type_word, thi, main_verb, neg
    # def get_neg(self, tokens):
    #     return 0

    def process(self, sentence):
        # sys.modules[__name__].__dict__.clear()
        # Process
        PRONOUN = 0
        NEG = 0
        WORD_COUNT = False
        counts = []
        vi_sentence = []
        eng_sentence = []
        list_chars = []
        proper_noun = []
        # 1. Nhập câu đầu vào
        sequence = sentence
        # 2. Tách từ câu đầu vào
        tokens = vn_token_uts(sequence)
        # 3.1 Lấy dữ liệu từ, loại từ, thì và động từ chính từ hàm
        word_list_vi, word_type_vi, tense, primary_idx, NEG = self.get_word_type_vi(tokens)
        for idx, word in enumerate(word_list_vi):
            print(word+" "+word_type_vi[idx])
        # primary_idx = 1
        print("Primary",primary_idx)
        print("NEG", NEG)
        # Alt.
        # primary_idx = 4
        # NEG = self.get_neg(tokens)
        # 4. Ánh xạ từ loại A-V và tìm từ tương ứng trong TA
        # vi_sentence = ((tu1,(loaitu1, 1)), (tu2,(loaitu2, 2)), ...)
        for idx, token in enumerate(word_list_vi):
            vi_sentence.append([token,[word_type_vi[idx], idx]])
        # print(vi_sentence)
        # eng_sentence = ((tu1,(loaitu1, 1)), (tu2,(loaitu2, 2)), ...)
        idx = 0
        list_words = []
        possesive_flag = False
        try:
            for sodem, word in enumerate(vi_sentence):
                k, v = word[0], word[1]
                c = []
                flag = 0
                idx+=1
                # print("ATT",v[0])
                # 4.1 Nếu là ký tự, bỏ qua
                if v[0] == 'kitu':
                    c.append(k)
                    eng_sentence.append([c,['kitu', idx]])
                    continue
                # 4.2 Nếu là tên riêng, bỏ qua
                if v[0] == 'daituxungho' and k[0].isupper():
                    c.append(k)
                    # print(c)
                    eng_sentence.append([c,['proper', idx]])
                    proper_noun.append(k)
                    continue
                # 4.3 Nếu là xuất hiện từ của, đưa về possessive noun
                if sodem < len(vi_sentence)-1:
                    if k == 'của' and vi_sentence[sodem+1][1][0] == 'daituxungho':
                        possesive_flag = True
                        c.append(k)
                        eng_sentence.append([c,['possesive', idx]])
                        continue
                for idx_en, i in enumerate(self.vi_eng_dict):
                    if k == i['word']:
                        print(i)
                        list_chars.append(i)
                        vi_type = v[0].strip()
                        # print(vi_type)
                        # 4.4 Nếu tồn tại loại từ phù hợp A-V
                        if vi_type in WTYPE_MATCH:
                            # print(WTYPE_MATCH.get(vi_type))
                            # 4.5 Nếu tồn tại loại từ phù hợp trên trong từ điển
                            # print(i['type'])
                            type_match = WTYPE_MATCH.get(vi_type)
                            if vi_type[0:5] == "photu":
                                type_match = type_match[:-1]
                            if 'type' in i and type_match in i['type']: 
                                # print("cc")
                                trans_idx = 0
                                res = {}
                                name_trans = ""
                                for type in i['type']:
                                    if 'trans'+str(trans_idx) in i:
                                        res.update(type=i['trans'+str(trans_idx)])
                                        if type == type_match:
                                            name_trans = 'trans'+str(trans_idx)
                                    else:
                                        trans_idx+=1
                                        res.update(type=i['trans'+str(trans_idx)])
                                        if type == type_match:
                                            name_trans = 'trans'+str(trans_idx)
                                    trans_idx+=1
                                print(name_trans)
                                list_words = i[name_trans].copy()
                                # print(list_words)
                                eng_sentence.append([list_words,[WTYPE_MATCH.get(vi_type), idx]])
                                flag = 1
                            # 4.5 Nếu từ điển không chứa loại từ tương ứng cho từ có được
                            else:
                                list_words = []
                                for key in i.keys():
                                    if key[0:3] == 'tra':
                                        for obj in i.get(key):
                                            list_words.append(obj)
                                eng_sentence.append([list_words,[WTYPE_MATCH.get(vi_type), idx]])
                                flag = 2
                        # 4.5 Không tìm được luật liên kết 2 loại từ A-V
                        else:
                            list_words = []
                            for key in i.keys():
                                if key[0:3] == 'tra':
                                    for obj in i.get(key):
                                        list_words.append(obj)
                            eng_sentence.append([list_words,["manytype", idx]])
                            flag = 3
                # 4.6 Không tìm được từ trong từ điển
                if flag == 0:
                    eng_sentence.append([k,["NA", idx]])
        except Exception:
                print('Error')
        # 6. Xử lý danh từ và chủ ngữ
        # 6.1 Xử lý danh từ có xuất hiện từ 'của'
        print(eng_sentence)
        try:
            for index, word in enumerate(eng_sentence):
                if word[1][0] == 'possesive' and possesive_flag:
                    pos_idx_en = word[1][1]
                    pos_idx_vi = pos_idx_en
                    # pos_word = word[0][0]
                    # print(pos_word)
                    for indx, i in enumerate(eng_sentence):
                        if i[1][0] == 'pronoun' and  i[1][1] > pos_idx_en:
                            # print(i[0][0])
                            # print(POSSESIVE.get("I"))
                            eng_sentence[indx][0][0] = POSSESIVE.get(i[0][0])
                            word[0][0] = ""
                            word[1][0] = None
                            for dtu_idx in range(index, -1, -1):
                                if eng_sentence[dtu_idx][1][0] == 'noun' or eng_sentence[dtu_idx][1][0] == 'pronoun':
                                    eng_sentence[dtu_idx][0][0] = eng_sentence[indx][0][0] + " " + eng_sentence[dtu_idx][0][0]
                                    eng_sentence[indx][0][0] = " "
                                    eng_sentence[indx][1][0] = None
                                    break
                        if i[1][0] == 'proper' and  i[1][1] > pos_idx_en:
                            for dtu_idx in range(index, -1, -1):
                                if eng_sentence[dtu_idx][1][0] == 'noun' or eng_sentence[dtu_idx][1][0] == 'pronoun':
                                    eng_sentence[dtu_idx][0][0] = self.no_accent_vietnamese(eng_sentence[indx][0][0]) + "'s " + eng_sentence[dtu_idx][0][0]
                                    eng_sentence[indx][0][0] = " "
                                    eng_sentence[indx][1][0] = None
                                    word[0][0] = ""
                                    word[1][0] = None
                                    break
                if index > primary_idx-1 and word[1][0] == 'number' and word[0][0] != 'one' and word[0][0] != 'a':
                    for indx in range (index, len(eng_sentence)):
                        if eng_sentence[indx][1][0] == 'noun':
                            eng_sentence[indx][0][0] = self.plural[self.singular.index(eng_sentence[indx][0][0])]
        except Exception:
                print('Error')

        print(eng_sentence)
        # 6.2 Xử lý tìm ngôi của chủ ngữ
        MANY_N = False
        I_flag = False
        try:
            for i in range(0, primary_idx):
                type_vi = vi_sentence[i][1][0]
                type_en = eng_sentence[i][1][0]
                word_en = eng_sentence[i][0][0]
                # print("")
                # print(vi_sentence[i][1][0])
                # print(eng_sentence[i][1][0])
                # print(eng_sentence[i][0][0])
                # 6.2.1 Nếu tồn tại quan hệ từ liệt kê
                if type_vi == 'quanhetulietke':
                    PRONOUN = 1
                    I_flag = False
                    break
                # 6.2.2 Nếu tồn tại lượng từ
                if type_vi == 'luongtu' and word_en != 'one' and word_en != 'a':
                    print(word_en)
                    for j in range (i, primary_idx):
                        if eng_sentence[j][1][0] == 'noun':
                            if len(eng_sentence[j][0][0].split()) > 1:
                                # print("CCCCCCCCC", eng_sentence)
                                main_noun = ' '.join(map(str, eng_sentence[j][0][0].split()[1:]))
                                eng_sentence[j][0][0] = eng_sentence[j][0][0].split()[0] + " " + self.plural[self.singular.index(main_noun)]
                            else:
                                eng_sentence[j][0][0] = self.plural[self.singular.index(eng_sentence[j][0][0])]
                            PRONOUN = 1
                            break
                # 6.2.3 Nếu tồn tại tên riêng
                if type_en == 'proper':
                    continue
                # 6.2.4 Nếu tồn tại đại từ số nhiều
                if type_en == 'pronoun':
                    if word_en == "I":
                        I_flag = True
                    if word_en != 'I':
                        word_en = word_en.lower()
                    for j in self.pronoun[1].values():
                        for smt in j:
                            if word_en == smt:
                                PRONOUN = 1
                                break
                        if PRONOUN:
                            break # TODO
                    # if PRONOUN:
                    #     break
                # 6.2.5 Nếu tồn tại danh từ không đếm được
                if word_en in self.uncount_noun:
                    continue
                # print(word_en)
                # 6.2.6 Nếu tồn tại danh từ số nhiều
                if word_en in self.plural:
                    PRONOUN = 1
                    break
                # 6.2.7 Nếu tồn tại số từ hoặc lượng từ
                if type_en == 'number' and word_en.lower() != 'one' and word_en.lower() != 'a' and eng_sentence[i+1][1][0] == 'noun':
                    MANY_N = True
                    continue
                if type_en == 'noun' and MANY_N:
                    PRONOUN = 1
                    # print(self.singular.index(word_en))
                    eng_sentence[i][0][0] = self.plural[self.singular.index(word_en)]
                    break

        except Exception:
                print('Error') 

        # 7. Chia động từ
        print(eng_sentence)
        try: 
            verb = eng_sentence[primary_idx][0][0]
            ext_flag = False
            ext_word = ""
            splited = verb.split(" ")
            # 7.0 Xử lý từ ngoại lai
            if len(splited) > 1:
                verb = splited[0]
                ext_flag = True
                for i in range (1, len(splited)):
                    ext_word+=splited[i]
                    if i != len(splited)-1:
                        ext_word+=' '
            v_type = eng_sentence[primary_idx][1][0]
            # print(eng_sentence)
            # print("dp", primary_idx)
            # print("Verb day nay",verb)
            # print(v_type)
            print("Pronoun", PRONOUN)
            # 7.1 Có động từ là không phải là 'be'
            if v_type == 'verb' and verb != "be":
                if tense == 'present':
                    if PRONOUN == 0 and I_flag == False:
                        if NEG == 0:
                            for v in self.verbs:
                                if v[0] == verb:
                                    eng_sentence[primary_idx][0][0] = v[1]
                                    break
                        else:
                            for v in self.verbs:
                                if v[0] == verb:
                                    eng_sentence[primary_idx][0][0] = "does not "+v[0]
                                    break
                    else:
                        if NEG == 0:
                            for v in self.verbs:
                                if v[0] == verb:
                                    eng_sentence[primary_idx][0][0] = v[0]
                                    break
                        else:
                            for v in self.verbs:
                                if v[0] == verb:
                                    eng_sentence[primary_idx][0][0] = "do not "+v[0]
                                    break
                elif tense == 'past':
                    for v in self.verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0][0] = v[2]
                                break
                            else:
                                eng_sentence[primary_idx][0][0] = "did not "+v[0]
                                break
                elif tense == 'future':
                    for v in self.verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence[primary_idx][0][0] = 'will '+v[0]
                                break
                            else:
                                eng_sentence[primary_idx][0][0] = 'will not '+v[0]
                                break
                elif tense == 'continous':
                    if PRONOUN == 0:
                        for v in self.verbs:
                            if v[0] == verb:
                                if NEG == 0:
                                    eng_sentence[primary_idx][0][0] = "is "+v[4]
                                    break
                                else:
                                    eng_sentence[primary_idx][0][0] = "is not "+v[4]
                                    break
                    elif I_flag == False:
                        for v in self.verbs:
                            if v[0] == verb:
                                if NEG == 0:
                                    eng_sentence[primary_idx][0][0] = "are "+v[4]
                                    break
                                else:
                                    eng_sentence[primary_idx][0][0] = "are not "+v[4]
                                    break
                    else:
                        for v in self.verbs:
                            if v[0] == verb:
                                if NEG == 0:
                                    eng_sentence[primary_idx][0][0] = "am "+v[4]
                                    break
                                else:
                                    eng_sentence[primary_idx][0][0] = "am not "+v[4]
                                    break
                try:
                    if verb in TO_VERB and eng_sentence[primary_idx+1][1][0] == 'verb':
                        eng_sentence[primary_idx][0][0] += " " + "to"
                except Exception:
                    print("Error")
            # 7.2 Không có động từ
            elif verb != "be":
                if tense == 'present':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence.insert(primary_idx, [['is'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                # print(eng_sentence[w][0])
                                if eng_sentence[w][0][0] != 'is':
                                    eng_sentence[w][1][1] += 1
                            # eng_sentence[primary_idx+1][0][0] = "is "+verb
                        else:
                            eng_sentence.insert(primary_idx, [['is not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'is not':
                                    eng_sentence[w][1][1] += 1
                    elif I_flag == False:
                        if NEG == 0:
                            eng_sentence.insert(primary_idx, [['are'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'are':
                                    eng_sentence[w][1][1] += 1
                        else:
                            eng_sentence.insert(primary_idx, [['are not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'are not':
                                    eng_sentence[w][1][1] += 1
                    else:
                        if NEG == 0:
                            eng_sentence.insert(primary_idx, [['am'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'am':
                                    eng_sentence[w][1][1] += 1
                        else:
                            eng_sentence.insert(primary_idx, [['am not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'am not':
                                    eng_sentence[w][1][1] += 1
                elif tense == 'past':
                    if NEG == 0:
                        if PRONOUN == 0:
                            eng_sentence.insert(primary_idx, [['was'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'was':
                                    eng_sentence[w][1][1] += 1
                        else:
                            eng_sentence.insert(primary_idx, [['were'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'were':
                                    eng_sentence[w][1][1] += 1
                    else:
                        if PRONOUN == 0:
                            eng_sentence.insert(primary_idx, [['was not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'was not':
                                    eng_sentence[w][1][1] += 1
                        else:
                            eng_sentence.insert(primary_idx, [['were not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'were not':
                                    eng_sentence[w][1][1] += 1
                elif tense == 'future':
                    for v in self.verbs:
                        if v[0] == verb:
                            if NEG == 0:
                                eng_sentence.insert(primary_idx, [['will be'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'will be':
                                    eng_sentence[w][1][1] += 1
                            else:
                                eng_sentence.insert(primary_idx, [['will not be'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'will not be':
                                    eng_sentence[w][1][1] += 1
                elif tense == 'continous':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence.insert(primary_idx, [['is'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'is':
                                    eng_sentence[w][1][1] += 1
                        else:
                            eng_sentence.insert(primary_idx, [['is not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'is not':
                                    eng_sentence[w][1][1] += 1
                    elif I_flag == False:
                        if NEG == 0:
                            eng_sentence.insert(primary_idx, [['are'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'are':
                                    eng_sentence[w][1][1] += 1
                        else:
                            eng_sentence.insert(primary_idx, [['are not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'are not':
                                    eng_sentence[w][1][1] += 1
                    else:
                        if NEG == 0:
                            eng_sentence.insert(primary_idx, [['am'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'am':
                                    eng_sentence[w][1][1] += 1
                        else:
                            eng_sentence.insert(primary_idx, [['am not'],['verb',primary_idx+1]])
                            for w in range(primary_idx, len(eng_sentence)):
                                if eng_sentence[w][0][0] != 'am not':
                                    eng_sentence[w][1][1] += 1
            # 7.2 Động từ là từ be
            else:
                if tense == 'present':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "is")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "is not")
                            eng_sentence[primary_idx][1][0] = "verb"
                    elif I_flag == False:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "are")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "are not")
                            eng_sentence[primary_idx][1][0] = "verb"
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "am")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "am not")
                            eng_sentence[primary_idx][1][0] = "verb"
                elif tense == 'past':
                    if NEG == 0:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "was")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "were")
                            eng_sentence[primary_idx][1][0] = "verb"
                    else:
                        if PRONOUN == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "was not")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "were not")
                            eng_sentence[primary_idx][1][0] = "verb"
                elif tense == 'future':
                    if NEG == 0:
                        eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", 'will be')
                        eng_sentence[primary_idx][1][0] = "verb"
                    else:
                        eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", 'will not be')
                        eng_sentence[primary_idx][1][0] = "verb"
                elif tense == 'continous':
                    if PRONOUN == 0:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "is")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "is not")
                            eng_sentence[primary_idx][1][0] = "verb"
                    elif I_flag == False:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "are")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "are not")
                            eng_sentence[primary_idx][1][0] = "verb"
                    else:
                        if NEG == 0:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "am")
                            eng_sentence[primary_idx][1][0] = "verb"
                        else:
                            eng_sentence[primary_idx][0][0] = eng_sentence[primary_idx][0][0].replace("be", "am not")
                            eng_sentence[primary_idx][1][0] = "verb"
        except Exception:
                print('Error')
        # 7.4 Chèn từ ngoại lai vào động từ
        try:
            if ext_flag:
                eng_sentence[primary_idx][0][0] += " "+ext_word
        except Exception:
                print('Error')
        print(eng_sentence)
        # 8. Sắp xếp lại cấu trúc câu
        for index, word in enumerate(eng_sentence):
            # 8.1 Tính từ đứng trước danh từ
            try:
                # if index < len(eng_sentence)-1:
                #     next_word = eng_sentence[index+1]
                if word[1][0] == 'adj':
                    adj_idx_en = word[1][1]
                    # print(adj_idx_en)
                    adj_idx_vi = adj_idx_en
                    # if adj_idx_en <
                    for i in range (adj_idx_en-1, -1, -1):
                        if eng_sentence[i][1][0] == 'noun':
                            adv_chr = eng_sentence[i][0][0].split(' ')
                            # print('CCCCCCCCCCCCCCCCCCCCCCCCCCC', adv_chr)
                            if adv_chr[0] in POSSESIVE_LIST:
                                eng_sentence[i][0][0] = eng_sentence[i][0][0].replace(adv_chr[0], adv_chr[0] + ' ' + word[0][0])
                            else:
                                eng_sentence[i][0][0] = word[0][0] + ' ' + eng_sentence[i][0][0]
                            word[0][0] = ""
                            word[1][0] = None
                            break
                        if eng_sentence[i][1][0] == 'verb':
                            eng_sentence[i][0][0] = eng_sentence[i][0][0] + " " + word[0][0] 
                            word[0][0] = ""
                            word[1][0] = None
                            break
            except Exception:
                print('Error')
            # 8.2 Trạng từ đứng trước danh, động, tính từ gần nhất mà nó bổ trợ
            if word[1][0] == 'advB' and word[0][0] != 'yesterday' and word[0][0] != 'today' and word[0][0] != 'tomorrow':
                adv_idx_en = word[1][1]
                adv_idx_vi = adv_idx_en
                for i in range (adv_idx_en-1, len(eng_sentence)):
                    if eng_sentence[i][1][0] == 'noun' or eng_sentence[i][1][0] == 'verb' or eng_sentence[i][1][0] == 'adj':
                        # print(eng_sentence[i][0][0])
                        # 8.2.1 Nếu là động từ và có từ ngoại lai, xử lý từ ngoại lai
                        if eng_sentence[i][1][0] == 'verb':
                            adv_chr = eng_sentence[i][0][0].split(' ')
                            if len(adv_chr) > 1:
                                if adv_chr[1] == 'not':
                                    eng_sentence[i][0][0] = adv_chr[0] + ' ' + adv_chr[1] + ' ' + word[0][0]
                                    for adv_idx, chr in enumerate(adv_chr):
                                        if adv_idx > 1:
                                            eng_sentence[i][0][0] += ' ' + chr
                                else:
                                    eng_sentence[i][0][0] = adv_chr[0] + ' ' + word[0][0]
                                    for adv_idx, chr in enumerate(adv_chr):
                                        if adv_idx > 0:
                                            eng_sentence[i][0][0] += ' ' + chr
                            else:
                                eng_sentence[i][0][0] = word[0][0] + ' ' + adv_chr[0]
                        else:
                            eng_sentence[i][0][0] = word[0][0] + ' ' + eng_sentence[i][0][0]
                        word[0][0] = ""
                        # print(word[1][0])
                        word[1][0] = None
                        break
            # 8.3 Trạng từ đứng sau danh, động, tính từ gần nhất mà nó bổ trợ
            try:
                if word[1][0] == 'advA':
                    adv_idx_en = word[1][1]
                    adv_idx_vi = adv_idx_en
                    for i in range (adv_idx_en-1, -1, -1):
                        if eng_sentence[i][1][0] == 'noun' or eng_sentence[i][1][0] == 'verb' or eng_sentence[i][1][0] == 'adj':
                            eng_sentence[i][0][0] =  eng_sentence[i][0][0] + " " + word[0][0]
                            word[0][0] = ""
                            word[1][0] = None
                            break
            except Exception:
                print('Error')
            # 8.4 Từ định danh đứng trước danh từ
            try:
                if word[1][0] == 'det':
                    det_idx_en = word[1][1]
                    det_idx_vi = det_idx_en
                    for i in range (det_idx_en-1, -1, -1):
                        if eng_sentence[i][1][0] == 'noun' :
                            eng_sentence[i][0][0] =  word[0][0] + " " + eng_sentence[i][0][0] 
                            word[0][0] = ""
                            word[1][0] = None
                            break
            except Exception:
                print('Error')
            # 8.5 Nếu có 2 danh từ liên tiếp, đảo vị trí cho nhau
            try:
                if word[1][0] == 'noun':
                    if eng_sentence[index][1][0] == 'noun':
                        word[0][0], eng_sentence[index][0][0] = eng_sentence[index][0][0], word[0][0]
            except Exception:
                print('Error')

            # if word[1][0] == 'possesive' and possesive_flag:
            #     print("CDGD")
            #     print(index)
            #     pos_idx_en = word[1][1]
            #     pos_idx_vi = pos_idx_en
            #     # pos_word = word[0][0]
            #     # print(pos_word)
            #     for indx, i in enumerate(eng_sentence):
            #         if i[1][0] == 'pronoun' and  i[1][1] > pos_idx_en:
            #             # print(i[0][0])
            #             # print(POSSESIVE.get("I"))
            #             eng_sentence[indx][0][0] = POSSESIVE.get(i[0][0])
            #     word[0][0] = ""
            #     word[1][0] = None

            # 8.6 Xử lý 'a', 'an' cho ngôi danh từ
            try:
                if word[0][0] == 'a':
                    try:
                        next_word = eng_sentence[index+1][0][0]
                        if next_word[0][0][0] in ['u', 'e', 'o', 'a', 'i']:
                            word[0][0] = 'an'
                            word[0][1] = 'a'
                    except:
                        word[0][0] = 'a'
            except Exception:
                print('Error')

        # 9. Trả về kết quả và các từ gợi ý
        result = ""
        for idx, i in enumerate(eng_sentence):
            if i[1][0] != None:
                # print(i[0][0].lower())
                if i[0][0] == "I":
                    result+="I "
                    continue
                if idx == 0 and i[1][0] != 'proper':
                    result+=i[0][0][0].upper()
                    result+=i[0][0][1:].lower()
                    result+=" "
                elif i[1][0] == 'proper':
                    result+=self.no_accent_vietnamese(i[0][0])+ ' '
                else:
                    result+=i[0][0].lower()
                    result+=" "
        print(result)
        result = result.strip()
        result = result
        print(result)
        return vi_sentence, eng_sentence, result, tense, list_chars
        
if __name__ == "__main__":
    my = MainProcess()
    vi_sentence, eng_sentence, result, tense, list_chars = my.process("Quang chạy rất nhanh")
    print(vi_sentence)
    print(eng_sentence)
    print(result)
    print(tense)
    # sentence = "mọi người đều thích điều này"
    # abc = get_token(sentence)
    # print(abc)