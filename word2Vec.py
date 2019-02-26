import gensim
import trt_doc as td

import numpy as np

# function that load our google pre-trained model, we had only used it once to load our model
def getPreTrainedModel():
    # Load Google's pre-trained Word2Vec model.
    model = gensim.models.KeyedVectors.load_word2vec_format('./word2vec/GoogleNews-vectors-negative300-SLIM.bin', binary=True)
    # model.save("word2vec/google_word2vec")
    # model.wv.save_word2vec_format("word2vec/word2vec_org",
    #                              "word2vec/vocabulary",
    #                              binary=False)

    return model

# function that calculates the average vector for a string
# calculates an average vector as the addition of all string's vectors divided by the number of vectors in that string
# @parameters : words : string ; model : our word2vec model ; num_features : dimension of a vector ; index2word_set : index of our vocabulary 
def mean_vector(words, model, num_features, index2word_set):
    # function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords > 0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

#function that calculates once and for all, the average vector for all our documents in the database
def Word2vec_avg_doc(filename):
    dict = []
    t = td.load_json(filename)
    for i in range(0, len(t)):
        t[i] = "".join(j for j in t[i] if not j.isdigit()) # In addition to tokenisation we omit all digits
        t[i] = td.cleanup(t[i]) # preprocess every word in every document in our data base
        doc_avg_vector = mean_vector(t[i].split(), model=model, num_features=300, index2word_set=index2word_set)
        dict.append(doc_avg_vector)
    np.save('word2vec/doc_vector.npy', dict) # we save our document's vectors once and for all to save time in calculus

#function that calculates for every query its average vector 
def Word2vec_avg_query(query):
    query_avg_vector = mean_vector(query.split(), model=model, num_features=300, index2word_set=index2word_set)
    return query_avg_vector

# function that calculates cosine similarity between 2 vectors
def cosine(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.sqrt(np.sum(v1**2)) * np.sqrt(np.sum(v2**2))) # mathematical formula

#function that calculates similarity between every document's vector in our data base and our query
def similarity(query):
    results = {}
    doc_vector = np.load('word2vec/doc_vector.npy') # We load our document's vectors
    query_vector = Word2vec_avg_query(query) # Calculate our query vector
    for i in range(1, len(doc_vector)):
        results[i] = cosine(doc_vector[i], query_vector) # calculating similarity between every document's vector in our data base and our query
    return results # results are saved in a dictionary

# function that sorts -and returns- our similarity's results saved in a dictionnary in decreasing order  
def get_results(query):
    a = similarity(query)
    s = sorted(a.items(), key=lambda t: t[1], reverse=True)
    return s

# Function that shows our results in our bottle server
def showResult(sortedDicoOfSimi):
    html = "<div class='result'><h3>Listes des resultats</h3>"
    for doc in sortedDicoOfSimi:
        html += "<div class='item'><a href='./doc/" + str(doc[0]) + "' >Document numero"+str(doc[0])+"</a><p>Similarite : "+str(doc[1])+"</p></div>"
    html += "</div>"
    return html

# We first load our saved model 
model = gensim.models.KeyedVectors.load('word2vec/google_word2vec')
# Indexing its vocabulary's words
index2word_set = set(model.wv.index2word)

