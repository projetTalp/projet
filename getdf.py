from nltk.stem import PorterStemmer

import sys
import math
import numpy as np
import random
import trt_doc as td
import json_gen

global motsVide


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


# TF comparison with idf :
def search_tf(request):
	req = td.cleanup(request)
	tmp = getOccurrenciesVector(req, motsVide)
	vectRequestTF = getTermFrenquency(tmp)
	descripteurs = td.load_json("data/tf.json")
	result = findSimilarite(descripteurs, vectRequestTF)
	return result
#############################


def getTFIdfResquest(req):
	req = td.cleanup(req)
	tmp = getOccurrenciesVector(req, motsVide)
	tf = getTermFrenquency(tmp)
	idf = td.load_json("data/idf.json")
	tf_idf = {}
	for word in tf:
		if idf.has_key(word):
			tf_idf[word] = tf[word] * idf[word]
	return tf_idf


def getTermFrenquency(frequencyVector):
	s = 0
	for i in frequencyVector:  # Recuperation du nombre de mots dans le doc
		s = s + frequencyVector[i]
	for i in frequencyVector:  # Calcul du tf pour chaque doc
		t = float(frequencyVector[i])/s
		frequencyVector[i] = round(t, 4)
	return frequencyVector


def similariteCos(vectDesc, vectReq):
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


def generateTF(filename):
	doc = td.loadDoc(filename)
	biblio = []
	for i in range (1, len(doc)):
		vect = getOccurrenciesVector(doc[i], motsVide)
		vect = getTermFrenquency(vect)
		biblio.append(vect)
	td.save_json(biblio, "data/tf.json")


def generateIDF(filename):
	tf_doc = td.load_json("data/tf.json")
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
	
	td.save_json(idf_tab, "data/idf.json")


def getTfIdfVector():
	"""Get the dictionnary which contains articles, then delete 'useless' words listed in the list motsVides
	to count how much times a word is present on a document"""
	tf = td.load_json("data/tf.json")
	idf = td.load_json("data/idf.json")
	tab = []
	for doc in tf:
		vectDoc = {}
		for word in doc:
			vectDoc[word] = doc[word] * idf[word]
		tab.append(vectDoc)
	td.save_json(tab, "data/tfidf.json")


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


def search(request):
	vectRequestIDF = getTFIdfResquest(request)
	descripteurs = td.load_json("data/tfidf.json")
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


def liste_inversee(filename):

	return 0



def main():
	# FOR TESTS
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
		json_gen.generate_JSON_DataBase()
		print("ok ?")
	return 0


motsVide = td.load_empty_words("data/motsvides.txt")


liste_inversee("data/tf.json")