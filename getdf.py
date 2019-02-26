from nltk.stem import PorterStemmer
import math
import numpy as np
import random
import trt_doc as td


global motsVide
global descripteurs
global idf

############################################################################################
# For Tests :
# Random tests
def get_sim_random():
	"""Give random similarity to documents for a special request, for test only"""
	dic = {}
	doc = td.load_json("data/database.json")
	for i in range(0, len(doc)):
		a = random.random()
		dic[i] = a
	return dic


def search_tf(request):
	"""" TF comparison with idf :"""
	req = td.cleanup(request)
	tmp = getOccurrenciesVector(req, motsVide)
	vectRequestTF = getTermFrenquency(tmp)
	descripteurtf = td.load_json("data/tf.json")
	result = findSimilarite(descripteurtf, vectRequestTF)
	return result
#############################


def getTFIdfResquest(req):
	"""Return the tf idf of a request"""
	req = td.cleanup(req)
	tmp = getOccurrenciesVector(req, motsVide)
	tf = getTermFrenquency(tmp)
	tf_idf = {}
	for word in tf:
		if idf.has_key(word):
			tf_idf[word] = tf[word] * idf[word]
	return tf_idf


def getTermFrenquency(frequencyVector):
	"""Return the term of a vector"""
	s = 0
	for i in frequencyVector:  # Recuperation du nombre de mots dans le doc
		s = s + frequencyVector[i]
	for i in frequencyVector:  # Calcul du tf pour chaque doc
		t = float(frequencyVector[i])/s
		frequencyVector[i] = round(t, 4)
	return frequencyVector


def similariteCos(vectDesc, vectReq):
	"""Calculate the cosinus simmilairy of a request and a descriptor"""
	prodScal = 0
	for word in vectReq:
		if vectDesc.has_key(word):
			prodScal = prodScal + vectDesc[word] * vectReq[word]
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


def cosine(v1, v2):
	""" Intermediate calcul for cosinus similarity"""
	v1 = np.array(v1)
	v2 = np.array(v2)
	return np.dot(v1, v2) / (np.sqrt(np.sum(v1**2)) * np.sqrt(np.sum(v2**2)))


def findSimilarite(vectRequestIDF, id_descripteur):
	""" Get the similarity of an idf request and a descriptor using cosinus similarity method"""
	result = {}
	i = 1
	for vectDesc in id_descripteur:
		result[vectDesc] = similariteCos(descripteurs[vectDesc-1], vectRequestIDF)
	return result


def normeVect(dic):
	norm = 0
	for i in dic:
		norm = norm + (float(dic[i]))**2
	norm = math.sqrt(norm)
	return norm


def search(request):
	"""Used by application to research best document of a request"""
	vectRequestIDF = getTFIdfResquest(request)
	mots = vectRequestIDF.keys()
	tab = {}
	for i in mots:
		for doc in liste_inverse[i]:
			tab[doc] = True
	result = findSimilarite(vectRequestIDF, tab)
	return result


def sortResult(dicoOfSimilarite):
	"""Used to sort result given by search to show the most similar at first"""
	s = sorted(dicoOfSimilarite.items(), key=lambda t: t[1], reverse=True)
	return s


def showResult(sortedDicoOfSimi):
	html = "<div class='result'><h3>Listes des resultats</h3>"
	for doc in sortedDicoOfSimi:
		html += "<div class='item'><a href='./doc/" + str(doc[0]) + "' >Document numero"+str(doc[0])+"</a><p>Similarite : "+str(doc[1])+"</p></div>"
	html += "</div>"
	return html


motsVide = td.load_empty_words("data/motsvides.txt")
descripteurs = td.load_json("data/tfidf.json")
idf = td.load_json("data/idf.json")
liste_inverse = td.load_json("data/liste_inverse.json")


