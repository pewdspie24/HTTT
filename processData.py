import re
import json

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

