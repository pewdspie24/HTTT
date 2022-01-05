import json
from underthesea import word_tokenize as vn_token_uts

def get_token(text):
    final = ""
    for word in text:
        final += word
        final += " "
    return final

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

    # Vietnamese loading
    for idx, i in enumerate(vi_eng_dict):
        try:
            a = i["word"]
            # TODO: trans1 without trans0 and "Như"
        except Exception as e:
            print(vi_eng_dict[idx])
            print(idx)
            
    # Process
    # while True:
    #     sequence = input()
    #     tokens = vn_token_uts(sequence)


    # sentence = "mọi người đều thích điều này"
    # abc = get_token(sentence)
    # print(abc)
