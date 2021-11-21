from underthesea import word_tokenize as vn_token_uts

# from vncorenlp import VnCoreNLP
# def vn_token_vnc(text):
#     annotator = VnCoreNLP("HTTT_Prj\VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g') 
#     word_segmented_text = annotator.tokenize(text)[0]
#     final = []
#     for word in word_segmented_text:
#         word = word.replace('_', ' ')
#         final.append(word)
#     return final

path = ["thantu.txt", "sotu.txt", "luongtu.txt", "danhtu.txt", "tinhtu.txt", "chitu.txt", "quanhetudinhvi.txt", "daitu.txt",  "dongtu.txt", "photu.txt"]
word_type = []
for id, i in enumerate(path):
    with open("viet_dict/" + i, encoding="utf-8") as f:
        s_type = f.readlines()
    for idx, i in enumerate(s_type):
        s_type[idx] = i.strip()
    word_type.append(s_type)

sentence = "ngày sau"
splited_word = vn_token_uts(sentence) 
len_sen = len(splited_word)
print(splited_word)
type_word = {}
thi = ""
for i in splited_word:
    ss = []
    for idx, j in enumerate(word_type):
        if i in j:
            ss.append(path[idx][:-4])
            check = 1
    if ss == i+ ": ":
        if i[0].isupper():
            ss.append(path[idx][:-4])
        else:
            ss.append("null")
    ss.append(str(idx))
    type_word[i] = ss
print(type_word)
# danh tu, dong tu
# tinh tu, dong tu
# for k, i in type_word.items():
#     if len(i) == 2:
#         if(i[0]) == "quanhetu":
        
