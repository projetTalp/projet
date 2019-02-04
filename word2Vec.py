import gensim as gm
import json_gen as js
import trt_doc as td
from nltk.stem import PorterStemmer

def getWordVector(filename, motsVides):
    vector=[]
    t = js.loadDoc(filename)
    for i in range(0, len(t)):
        for word in t[i] :
            if word != '' :  # Empty word check
                if word not in motsVides:  # Useless word check
                    ps = PorterStemmer()  # Stem the word to simplify query in the future
                    word = ps.stem(word)
                    vector.append(word)
    return vector

def trainWord2VecDict(vector):
    model = gm.Word2Vec(vector, min_count=0)
    td.save_json(model, "data/word2VecDict.json")

