import gensim
import json_gen as js
import trt_doc as td

import numpy as np



""""
def getWordVector(filename):
    vector=[]
    t = td.load_json(filename)
    for i in range(0,len(t)):
        for cle in t[i].keys():
            vector.append(cle)
    return vector

def trainWord2VecDict(vector):

    model = Word2Vec(vector, min_count=0)
    return model
"""


def getPreTrainedModel():
    # Load Google's pre-trained Word2Vec model.
    model = gensim.models.KeyedVectors.load_word2vec_format('./word2vec/GoogleNews-vectors-negative300-SLIM.bin', binary=True)
    # model.save("word2vec/google_word2vec")
    # model.wv.save_word2vec_format("word2vec/word2vec_org",
    #                              "word2vec/vocabulary",
    #                              binary=False)

    return model




def mean_vector(words, model, num_features,index2word_set):
    #function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords>0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

def Word2vec_avg_doc (filename) :
    dict = []
    tmp=[]
    doc_avg_vector=0
    t = td.load_json(filename)
    for i in range(0,len(t)):
        t[i] = "".join(j for j in t[i] if not j.isdigit())
        t[i] = td.cleanup(t[i])
        doc_avg_vector = mean_vector(t[i].split(), model=model, num_features=300, index2word_set=index2word_set)
        dict.append(doc_avg_vector)
    np.save('word2vec/doc_vector.npy', dict)

def Word2vec_avg_query (query) :

    query_avg_vector = mean_vector(query.split(), model=model, num_features=300, index2word_set=index2word_set)
    return query_avg_vector


def cosine(v1, v2):
	v1 = np.array(v1)
	v2 = np.array(v2)
	return np.dot(v1, v2) / (np.sqrt(np.sum(v1**2)) * np.sqrt(np.sum(v2**2)))

def similarity (query) :
    results = {}
    doc_vector=np.load('word2vec/doc_vector.npy')
    query_vector=Word2vec_avg_query(query)
    for i in range(0,len(doc_vector)):
        results[i]=cosine(doc_vector[i],query_vector)
    return results

def get_results(query):
    a=similarity(query)
    s = sorted(a.items(), key=lambda t: t[1], reverse=True)
    return s

def showResult(sortedDicoOfSimi):
	html = "<div class='result'><h3>Listes des resultats</h3>"
	for doc in sortedDicoOfSimi:
		html += "<div class='item'><a href='./doc/" + str(doc[0]) + "' >Document numero"+str(doc[0])+"</a><p>Similarite : "+str(doc[1])+"</p></div>"
	html += "</div>"
return html






model = gensim.models.KeyedVectors.load('word2vec/google_word2vec')
index2word_set = set(model.wv.index2word)


#Word2vec_avg_doc ("data/CISI.ALL.json")

#print(show_results(" Why should hello "))
