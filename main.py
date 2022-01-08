from underthesea import word_tokenize as vn_token_uts
from vncorenlp import VnCoreNLP

def vn_token_vnc(text):
    annotator = VnCoreNLP("HTTT_Prj\VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g') 
    word_segmented_text = annotator.tokenize(text)[0]
    final = []
    for word in word_segmented_text:
        word = word.replace('_', ' ')
        final.append(word)
    return final

sentence = "tôi vô cùng bực"
abc = vn_token_uts(sentence) 
print(abc)
