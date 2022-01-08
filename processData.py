import re
import json
from googletrans import Translator
translator = Translator()

with open("dict.txt", encoding="utf8", mode="r") as f:
    a = f.readlines()
dictList = []
aDict={}
flag = 0

for i in a:
    if i == "\n":
        dictList.append(aDict)
        aDict = {}
        flag = 0
    elif i[0] == '@':
        aDict.update({"word":i[1:].strip('\n')})
    elif i[0] == '*':
        if 'type' in aDict:
            tmp_list = aDict.get('type')
            tmp_list.append(i[2:].strip('\n'))
            aDict.update({"type":tmp_list})
        else:
            tmp_list = []
            tmp_list.append(i[2:].strip('\n'))
            aDict.update({"type":tmp_list})
        flag += 1
    elif i[0] == '-':
        if 'trans'+str(flag) in aDict:
            tmp_trans = aDict.get("trans"+str(flag))
            tmp = i[2:].strip('\n')
            pattern = '%s(.*?)%s' % (re.escape('('), re.escape(')'))
            tmp = re.sub(pattern,'',tmp)
            tmp = re.split('[,;]+', tmp)
            tmp = [x.strip(' ') for x in tmp]
            result = []
            for i in tmp:
                if i[0:3].lower() == 'to ':
                    result.append(i[3:])
                else:
                    result.append(i)
            tmp_trans.extend(result)
            aDict.update({"trans"+str(flag):tmp_trans})
        else:
            # tmp_trans = []
            tmp = i[2:].strip('\n')
            pattern = '%s(.*?)%s' % (re.escape('('), re.escape(')'))
            tmp = re.sub(pattern,'',tmp)
            tmp = re.split('[,;]+', tmp)
            tmp = [x.strip(' ') for x in tmp]
            result = []
            for i in tmp:
                if i[0:3].lower() == 'to ':
                    result.append(i[3:])
                else:
                    result.append(i)
            # tmp_trans.append(tmp)
            aDict.update({"trans"+str(flag):result})

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dictList, f, ensure_ascii=False, indent=4)            

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

# Vietnamese loading
for idx, i in enumerate(vi_eng_dict):
    # try:
    for postfix in range (0,7):
        if "trans"+str(postfix) in i:
            if i["trans"+str(postfix)][0][0:3] == "như" or i["trans"+str(postfix)][0][0:3] == "Như":
                # print(i["trans"+str(postfix)][0][4:])
                print(i["trans"+str(postfix)][0][4:])
                i["trans"+str(postfix)][0] = translator.translate(i["trans"+str(postfix)][0][4:], src="vi", dest="en").text
                print(i["trans"+str(postfix)][0])
            # TODO: trans1 without trans0 and "Như"
    # except Exception as e:
    #     print(vi_eng_dict[idx])
    #     print(idx)
with open("testing.json", "w", encoding='utf-8') as outfile:
    json.dump(vi_eng_dict, outfile, ensure_ascii=False, indent=4)   

aux_list = []
for i in vi_eng_dict:
    if 'type' in i:
        for a in i['type']:
            if a not in aux_list:
                aux_list.append(a)
for i in aux_list:
    print(i)