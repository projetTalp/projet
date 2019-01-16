from nltk.stem import PorterStemmer

import json
import sys
import math
import numpy as np


global motsVide


def getDoc(file, id):
	f = open(file, "r")
	t = (f.read().split(".I "))[id]
	f.close()
	return t


def loadDoc(file):
	"""Open target file and split it according to the differents ligne .I.
Then, replace some character with space to avoid problems."""
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


def cleanQueryVector(query, motsVides):
	"""Delete empty word and Stem words on the query"""
	query = query.split(" ")
	cleanedQuery = []  # List of correct word
	for i in query:
		if i != '':
			if i not in motsVides:  # Add on the list if not empty word
				ps = PorterStemmer()
				i = ps.stem(i)
				cleanedQuery.append(i)
	return cleanedQuery

def getTermFrenquency(frequencyVector):
	sum = 0
	for i in frequencyVector:  # Recuperation du nombre de mots dans le doc
		sum = sum + frequencyVector[i]
	for i in frequencyVector:  # Calcul du tf pour chaque doc
		t = float(frequencyVector[i])/sum
		frequencyVector[i] = round(t, 4)
	return frequencyVector


def loadMotsVides(file):
	f = open(file, 'r')
	t = f.readlines()
	for i in range(0, len(t)):
		t[i] = t[i].replace('\n', "")
	return t


def DC(descTable, word):
	cpt = 0
	for i in descTable :
		if word in i.keys():
			cpt+=1
	return cpt


def idf2(descTable, tabWord):
	n = len(descTable)
	tmp = {}
	for word in tabWord:
		dc = DC(descTable, word)
		if dc != 0:
			tmp[word] = math.log10(n/dc)
		else:
			tmp[word] = 0
	return tmp


def save_json(tab, file):
	txt = json.dumps(tab)
	f = open(file, "w")
	f.write(txt)
	f.close() 
	

	
def load_json(file):
	f = open(file, "r")
	txt = f.read()
	tab = json.loads(txt)
	return tab




def similariteCos(vectDesc, vectReq):
	prodScal = 0
	for word in vectReq:
		if vectDesc.has_key(word):
			prodScal = prodScal+ vectDesc[word] * vectReq[word]
	cos = prodScal / (normeVect(vectDesc) * normeVect(vectReq))
	return cos


def preprocessing(doc):
	motsVides = motsVide
	doc = doc.split(" ")
	tab=[]
	for i in doc:  # Read document
		if i != '':  # Empty word check
			if i not in motsVides:  # Useless word check
				i = i.lower()  # make all words lower case
				ps = PorterStemmer()  # Stem the word to simplify query in the future
				i = ps.stem(i)
				tab.append(i)
	return tab

def freq(word, doc):
	tab = preprocessing(doc)
	cpt = 0
	for i in range(0,len(tab)):
		if tab[i]== word:
			cpt +=0
	return cpt


def word_count(doc):
	tab = preprocessing(doc)
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


def generateTF(file, motsVide):
	doc = loadDoc(file)
	biblio = []
	for i in range (1, len(doc)):
		vect = getOccurrenciesVector(doc[i], motsVide)
		vect = getTermFrenquency(vect)
		biblio.append(vect)
	save_json(biblio, "tf.json")
	
def generateIDF(file):
	tf_doc = load_json("tf.json")
	idf_tab = []
	for doc in tf_doc:
		for word in doc:
			if idf_tab[word] is None:
				idf_tab[word] = 1
			else:
				idf_tab[word] += 1
	save_json(idf_tab, "idf.json")
	return


def getTfIdfVector(list_of_docs):
	"""Get the dictionnary which contains articles, then delete 'useless' words listed in the list motsVides
	to count how much times a word is present on a document"""
	tf = load_json("tf.json")
	idf = load_json("idf.json")
	tmp_doc = []
	dico={}

	for i in range(1,len(list_of_docs)+1): # Read document
		tmp_doc = preprocessing(list_of_docs[i])
		for word in tmp_doc:
			if dico[i][word] is None:
				dico[i][word] = tf[list_of_docs[i]][word] * idf[word]
	return dico


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
	vectRequestWord = cleanQueryVector(request, motsVide)
	descripteurs = load_json("descripteur.json")
	vectRequestIDF = idf(descripteurs, vectRequestWord)
	result = findSimilarite(descripteurs, vectRequestIDF)
	return result

def sortResult(dicoOfSimilarite):
	print(dicoOfSimilarite)
	s=sorted(dicoOfSimilarite, key=dicoOfSimilarite.__getitem__)
	print(s)
	return s
	
def showResult(sortedDicoOfSimi):
	html = "<div class='result'><h3>Listes des resultats</h3>"
	for doc in sortedDicoOfSimi:
		html += "<div class='item'><a href='./doc/" + str(doc) + "' >Document numero"+str(doc)+"</a><p>Similarite : "+str(sortedDicoOfSimi[doc])+"</p></div>"
	html += "</div>"
	return html
	


motsVide = loadMotsVides("motsvides.txt")


