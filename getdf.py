from nltk.stem import PorterStemmer

import json
import sys
import math
import numpy as np


global motsVide


def getDoc(file, id):
	"""Load a file and split it every time '.I' appear"""
	f = open(file, "r")
	t = (f.read().split(".I "))[id]
	f.close()
	return t


def loadDoc(file):
	"""Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems."""
	f = open(file, "r")
	t = f.read().split(".I ")
	for i in range(0, len(t)):  # Clean target file
		t[i] = t[i].replace('\n', " ")
		t[i] = t[i].replace(',', " ")
		t[i] = t[i].replace('.', " ")
		t[i] = t[i].replace('"', " ")
		t[i] = t[i].lower()
	f.close()
	return t


def load_empty_words(empty_word_list):
	"""Get word on the given list and build a list of them"""
	f = open(empty_word_list, 'r')
	t = f.readlines()
	for i in range(0, len(t)):
		t[i] = t[i].replace('\n', "")
	return t


def save_json(tab, fil):
	"""Save a json named tab into a file named fil"""
	txt = json.dumps(tab)
	f = open(fil, "w")
	f.write(txt)
	f.close()


def load_json(fil):
	"""Load a file named fil into local variable tab"""
	f = open(fil, "r")
	txt = f.read()
	tab = json.loads(txt)
	return tab


def text_cleanup(text):
	"""Delete empty word and Stem words on the query"""
	to_clean = text.split(" ")
	cleanedQuery = []  # List of correct word
	for i in to_clean:
		if i != '':
			if i not in motsVide:  # Add on the list if not empty word
				ps = PorterStemmer()
				i = ps.stem(i)
				cleanedQuery.append(i)
	return cleanedQuery


def getTFIdfResquest(req):
	tmp = getOccurrenciesVector(req, motsVide)
	tf = getTermFrenquency(tmp)
	idf = load_json("idf.json")
	tf_idf = {}
	for word in tf:
		if(idf.has_key(word)):
			tf_idf[word] = tf[word] * idf[word]
	return tf_idf


def getTermFrenquency(frequencyVector):
	sum = 0
	for i in frequencyVector:  # Recuperation du nombre de mots dans le doc
		sum = sum + frequencyVector[i]
	for i in frequencyVector:  # Calcul du tf pour chaque doc
		t = float(frequencyVector[i])/sum
		frequencyVector[i] = round(t, 4)
	return frequencyVector


def similariteCos(vectDesc, vectReq):
	prodScal = 0
	for word in vectReq:
		if vectDesc.has_key(word):
			prodScal = prodScal+ vectDesc[word] * vectReq[word]
	cos = prodScal / (normeVect(vectDesc) * normeVect(vectReq))
	return cos


def getOccurrenciesVector(doc, motsVides):
	"""Get the dictionnary which contains articles, then delete 'useless' words listed in the list motsVides
	to count how much times a word is present on a document"""
	doc = doc.split(" ")
	dico = {}
	for i in doc:  # Read document
		if i != '':  # Empty word check
			if i not in motsVides:  # Useless word check
				ps = PorterStemmer()  # Stem the word to simplify query in the future
				i = ps.stem(i)
				if dico.has_key(i):  # Count word
					dico[i] = dico[i]+1
				else:
					dico[i] = 1
	return dico



"""
def freq(word, doc):
	tab = text_cleanup(doc)
	cpt = 0
	for i in range(0, len(tab)):
		if tab[i] == word:
			cpt += 0
	return cpt
	
	
def word_count(doc):
	tab = text_cleanup(doc)
	return len(tab)


def tf(word, doc):
	return freq(word, doc) / float(word_count(doc))


def num_docs_containing(word, list_of_docs):
	count = 0
	for document in list_of_docs:
		if freq(word, document) > 0:
			count += 1
	return 1 + count


def idf(word, list_of_docs):
	return math.log(len(list_of_docs) /
		float(num_docs_containing(word, list_of_docs)))


def tf_idf(word, doc, list_of_docs):
	return (tf(word, doc) * idf(word, list_of_docs))
"""

def generateTF(file):
	doc = loadDoc(file)
	biblio = []
	for i in range (1, len(doc)):
		vect = getOccurrenciesVector(doc[i], motsVide)
		vect = getTermFrenquency(vect)
		biblio.append(vect)
	save_json(biblio, "data/tf.json")
	
def generateIDF(file):
	tf_doc = load_json("data/tf.json")
	nb_doc = len(tf_doc) + 1
	occ = {}
	for doc in tf_doc:
		for word in doc:
			if occ.has_key(word):
				occ[word] += 1
			else:
				occ[word] = 1
	idf_tab = {}
	for word in occ: 
		idf_tab[word] = math.log(nb_doc/occ[word])
	
	save_json(idf_tab, "idf.json")


def getTfIdfVector():
	"""Get the dictionnary which contains articles, then delete 'useless' words listed in the list motsVides
	to count how much times a word is present on a document"""
	tf = load_json("tf.json")
	idf = load_json("idf.json")
	tab = []
	for doc in tf:
		vectDoc={}
		for word in doc:
			vectDoc[word] = doc[word] * idf[word]
		tab.append(vectDoc)
	save_json(tab, "tfidf.json")


def cosine(v1, v2):
	v1 = np.array(v1)
	v2 = np.array(v2)
	return np.dot(v1, v2) / (np.sqrt(np.sum(v1**2)) * np.sqrt(np.sum(v2**2)))
"""
# Pour elargir notre BDD
def load_data():
    df = pd.read_csv(data_path)
    return df
def get_results(self, query, max_rows=10):
	score = self.get_score(query)
	results_df = copy.deepcopy(self.df)
	results_df['ranking_score'] = score
	results_df = results_df.loc[score > 0]
	results_df = results_df.iloc[np.argsort(-results_df['ranking_score'].values)]
	results_df = results_df.head(max_rows)
	self.print_results(results_df, query)
	return results_df

def similarities(self, list_of_words):
        ###Returns a list of all the [docname, similarity_score] pairs relative to a list of words. 
        
    # building the query dictionary
    query_dict = {}
    for w in list_of_words:
        query_dict[w] = query_dict.get(w, 0.0) + 1.0

    # normalizing the query
    length = float(len(list_of_words))
    for k in query_dict:
        query_dict[k] = query_dict[k] / length

    # computing the list of similarities
    sims = []
    for doc in self.documents:
        score = 0.0
        doc_dict = doc[1]
        for k in query_dict:
            if k in doc_dict:
                score += (query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k])
        sims.append([doc[0], score])

    return sims
"""

def findSimilarite(descripteurs, vectRequestIDF):
	result = {}
	i = 1 
	for vectDesc in descripteurs:
		result[i] = similariteCos(vectDesc, vectRequestIDF)
		i += 1
	return result


def normeVect(dic):
	norm = 0
	for i in dic:
		norm = norm + (float(dic[i]))**2
		norm = math.sqrt(norm)
	return norm


def main():
	
	mode = sys.argv[1]

	if mode == "-load":
		file = sys.argv[2]
		generateTF(file, motsVide)

	elif mode == "-search":
		request = sys.argv[2]
		result = search(request)
		return result
	return 0


def search(request):
	vectRequestIDF = getTFIdfResquest(request)
	descripteurs = load_json("tfidf.json")
	result = findSimilarite(descripteurs, vectRequestIDF)
	return result

def sortResult(dicoOfSimilarite):
	print(dicoOfSimilarite)
	s = sorted(dicoOfSimilarite.items(), key=lambda t: t[1], reverse=True)
	print(s)
	return s
	
def showResult(sortedDicoOfSimi):
	html = "<div class='result'><h3>Listes des resultats</h3>"
	for doc in sortedDicoOfSimi:
		html += "<div class='item'><a href='./doc/" + str(doc[0]) + "' >Document numero"+str(doc[0])+"</a><p>Similarite : "+str(doc[1])+"</p></div>"
	html += "</div>"
	return html


motsVide = load_empty_words("data/motsvides.txt")

#generateIDF("firstdata")
##getTfIdfVector()
