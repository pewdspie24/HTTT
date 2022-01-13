# WTYPE_MATCH = {'danhtuchung':'noun', 'dongtu':'verb', 'tinhtu':'adj', 'sotu':'number', 'luongtu':'adj', 'photu':'advA', 'photuchimucdo':'advB', 'photuthoigian':'advB', 'daitu':'pronoun', 'thantu':'excl', 'quanhetulietke':'conj', 'quanhetudinhvi':'prep', 'chitu':'det', 'daituxungho':'pronoun'}
# TENSE = ['present', 'past', 'future', 'continous']
# FLAG = 0
# PATH_VI = ["danhtuchiloai.txt", "dongtu.txt", "chitu.txt", "daituxungho.txt", "danhtuchung.txt", 
#         "luongtu.txt", "photuchimucdo.txt", "photuphudinh.txt", "photuthoigian.txt", 
#         "quanhetudinhvi.txt", "quanhetulietke.txt", "sotu.txt", "thantu.txt", "tinhtu.txt"]
# VI_DICT_PATH = "viet_dict/dict_chitiet/"
# word_type_vi = {}
# for i in PATH_VI:
#     with open(VI_DICT_PATH + i, "r+", encoding="utf-8" ) as f:
#         for line in f.readlines():
#             tmp = line.strip()
#             if tmp in word_type_vi:
#                 word_type_vi[tmp] += " " + i[:-4]
#             else:
#                 word_type_vi[tmp] = i[:-4]  
# for k, v in word_type_vi.items():
#     if len(v.split(" ")) > 1 and "dongtu" in v:
#         print(k + ": " + v) 
# import pandas
# nouns = pandas.read_csv("eng_dict\\noun.csv")
# plural = nouns['plural']
# singular = nouns['singular']
# s = "person"
# # if s in plural.values:
# df_new = nouns[(nouns.singular == s)]["plural"]
# print(df_new)
import numpy as np
from numpy.lib import type_check
tmp = ['daituxungho', 'danhtuchung dongtu tinhtu', 'dongtu quanhetudinhvi', 'danhtuchung', 'danhtuchung sotu']
type_word = ['daituxungho', ' dongtu tinhtu', 'quanhetudinhvi', 'danhtuchung', 'sotu']
check = not np.array_equal(tmp, type_word)
print(check)