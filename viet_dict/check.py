import  os
s = "Hôm    nay  tui đói lắm " # ""đơn vị cô ấy đi ăn cơm"" "quang học nhiều bài lắm"

path = ["thantu.txt", "sotu.txt", "luongtu.txt", "danhtu.txt", "tinhtu.txt", "chitu.txt", "quanhetu.txt", "daitu.txt",  "dongtu.txt", "photu.txt"]
        # "tagged-1.txt", "tagged-2.txt",  "tudien-ast.txt", "tudien.txt"
# for file in os.listdir("HTTT/viet_dict"):
#     path += '"'+ file + '", '
# print(path)

word_type = []
for id, i in enumerate(path):
    with open("D:/study4/HTDTTT/btl/HTTT/viet_dict/" + i, encoding="utf-8") as f:
        s_type = f.readlines()
    for idx, i in enumerate(s_type):
        s_type[idx] = i.strip()
    word_type.append(s_type)

splited_word = s.split()
len_sen = len(splited_word)
# print(splited_word)
# print(len_sen)
for i in range(len_sen):
    word = splited_word[i]
    # min
    # dem = 0
    # check = 0
    # while check == 0 and dem < len_sen:
    #     if dem != 0:
    #         word += " " + splited_word[dem]
    #     ss = word + ": "
    #     for idx, j in enumerate(word_type):
    #         if word in j:
    #             ss += path[idx][:-4] + ", "
    #             check = 1
    #     print(ss)
    
    # max   
    dem = 0
    check =0
    tmp = []
    while i+dem < len_sen:
        if dem != 0:
            word += " " + splited_word[i + dem]
        ss = word + ": "
        for idx, j in enumerate(word_type):     
            if word in j:
                ss += path[idx][:-4] + ", "   
                check = 1   
        if ss != word + ": ":
            tmp.append(ss)
        else: 
            if check == 1:
                break
        dem += 1
    print(tmp)
    # print(tmp[-1])
                

# 1. Các từ đã được tách và vị trí của nó
# 2. Thì của nó
# 3. Các từ thuộc chủ, các từ thuộc vị, vị trí động từ chính