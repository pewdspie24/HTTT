def get_word_type_vi(self, tokens):
        I_flag = False
        word = []
        type_word = []
        thi = "present"
        main_verb = 0 
        for token in tokens:
            try:
                type_word.append(self.word_type_vi[token])
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