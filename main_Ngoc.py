from underthesea import word_tokenize as vn_token_uts
link_add = "D:/study4/HTDTTT/btl/HTTT/viet_dict/"
word = {}
path = ["chitu.txt", "daitu.txt", "danhtu.txt", "dongtu.txt", "luongtu.txt", "photuchimucdo.txt", "photumenhlenh.txt", "photuphudinh.txt", 
        "photuthoigian.txt", "quanhetucouple.txt", "quanhetudinhvi.txt", "quanhetulietke.txt", "quanhetusosanh.txt", "sotu.txt", "thantu.txt", "tinhtu.txt"]

for i in path:
    with open(link_add + i, "r+", encoding="utf-8" ) as f:
        for line in f.readlines():
            tmp = line.strip()
            if tmp in word:
                word[tmp] += " " + i[:-4]
            else:
                word[tmp] = i[:-4]
                      
with open("type_of_word", "a", encoding="utf-8") as f:
    for k, v in word.items():
        typee = v.split(" ") 
        if len(typee) >1 :
            f.write(k + " " + v + "\n")
print("done")
# word_type = []
# for id, i in enumerate(path):
#     with open("D:/study4/HTDTTT/btl/HTTT/viet_dict/" + i, encoding="utf-8") as f:
#         s_type = f.readlines()
#     for idx, i in enumerate(s_type):
#         s_type[idx] = i.strip()
#     word_type.append(s_type)
    
# sentence = "anh ấy có lẽ thích cô ấy"
# splited_word = vn_token_uts(sentence) 
# len_sen = len(splited_word)
# print(splited_word)
# type_word = {}
# thi = ""
# for i in splited_word:
#     ss = []
#     for idx, j in enumerate(word_type):
#         if i in j:
#             ss.append(path[idx][:-4])
#             check = 1
#     if ss == i+ ": ":
#         if i[0].isupper():
#             ss.append(path[idx][:-4])
#         else:
#             ss.append("null")
#     ss.append(str(idx))
#     type_word[i] = ss
# print(type_word)
# # danh tu, dong tu
# # tinh tu, dong tu
# # for k, i in type_word.items():
# #     if len(i) == 2:
# #         if(i[0]) == "quanhetu":
        
