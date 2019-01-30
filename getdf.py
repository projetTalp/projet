from nltk.stem import PorterStemmer

import json
import sys
import math
import numpy as np


global motsVide


def getDoc(file, id):
	"""Load a file and split it every time '.I' appear"""
	# f = open(file, "r")
	# t = (f.read().split(".I "))[id]
	# f.close()
	t = load_json("data/database.json")[id]
	return t


def loadDoc(file):
	"""Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems."""
	t = load_json("data/database.json")
	for i in range(0, len(t)):  # Clean target file
		t[i] = cleanup(t[i])
	return t


def cleanup(string):
	string = string.replace('\n', " ")
	string = string.replace(',', " ")
	string = string.replace('.', " ")
	string = string.replace('"', " ")
	string = string.replace('(', " ")
	string = string.replace(')', " ")
	string = string.replace(']', " ")
	string = string.replace('[', " ")
	string = string.replace('/', " ")
	string = string.replace('\t', " ")
	string = string.replace('-', " ")
	string = string.replace('_', " ")
	string = string.replace('?', " ")
	string = string.replace('!', " ")
	string = string.replace('*', " ")
	string = string.replace(';', " ")
	string = string.lower()
	return string


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
	req = cleanup(req)
	tmp = getOccurrenciesVector(req, motsVide)
	tf = getTermFrenquency(tmp)
	idf = load_json("data/idf.json")
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
	normeReq = normeVect(vectReq)
	if normeReq != 0:
		cos = prodScal / (normeVect(vectDesc) * normeReq)
		return cos
	return 0


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
	
	save_json(idf_tab, "data/idf.json")


def getTfIdfVector():
	"""Get the dictionnary which contains articles, then delete 'useless' words listed in the list motsVides
	to count how much times a word is present on a document"""
	tf = load_json("data/tf.json")
	idf = load_json("data/idf.json")
	tab = []
	for doc in tf:
		vectDoc={}
		for word in doc:
			vectDoc[word] = doc[word] * idf[word]
		tab.append(vectDoc)
	save_json(tab, "data/tfidf.json")


def cosine(v1, v2):
	v1 = np.array(v1)
	v2 = np.array(v2)
	return np.dot(v1, v2) / (np.sqrt(np.sum(v1**2)) * np.sqrt(np.sum(v2**2)))



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
		generateTF("data/firstdata")
		generateIDF("data/firstdata")
		getTfIdfVector()

	elif mode == "-search":
		request = sys.argv[2]
		result = search(request)
		return result
	elif mode == "-selectDatabase":
		generate_JSON_DataBase()
		print("ok ?")
	return 0


def search(request):
	vectRequestIDF = getTFIdfResquest(request)
	descripteurs = load_json("data/tfidf.json")
	result = findSimilarite(descripteurs, vectRequestIDF)
	return result

def sortResult(dicoOfSimilarite):
	s = sorted(dicoOfSimilarite.items(), key=lambda t: t[1], reverse=True)
	return s
	
def showResult(sortedDicoOfSimi):
	html = "<div class='result'><h3>Listes des resultats</h3>"
	for doc in sortedDicoOfSimi:
		html += "<div class='item'><a href='./doc/" + str(doc[0]) + "' >Document numero"+str(doc[0])+"</a><p>Similarite : "+str(doc[1])+"</p></div>"
	html += "</div>"
	return html



def loadBaseFileProf(file):
	"""Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems."""
	f = open(file, "r")
	t = f.read().split(".I ")
	for i in range(0, len(t)):  # Clean target file
		a = t[i].split('\n')
		text = ""
		for z in range(1,len(a)):
			text = text + " " + a[z]
		t[i] = text
	f.close()
	save_json(t, file + ".json")
	
	
def loadBaseNYT(file):
	"""Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems."""
	f = open(file, "r")
	t = f.read().split("URL:")
	for i in range(0, len(t)):  # Clean target file
		a = t[i].split('\n')
		text = ""
		for z in range(1, len(a)):
			text = text + " " + a[z]
		t[i] = text
	f.close()
	save_json(t, "data/NYT.json")


def loadBaseCSV(file):
	"""Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems."""
	f = open(file, "r")
	t = f.read().split("\n")
	f.close()
	return t

def generate_JSON_DataBase():
	database = load_json("data/firstdata.json")# + load_json("data/NYT.json") ##TODO: choisir ici la bdd 
	save_json(database, "data/database.json")


motsVide = load_empty_words("data/motsvides.txt")

#loadBaseFileProf("data/firstdata")
#generate_JSON_DataBase()


