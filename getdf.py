from nltk.stem import PorterStemmer
import math

import json
import sys
import math


def loadDoc(file):
	f = open(file, "r")
	t = f.read().split(".I ")
	for i in range(0, len(t)) :
		t[i] = t[i].replace('\n', " ")
		t[i] = t[i].replace(',', " ")
		t[i] = t[i].replace('.', " ")
		t[i] = t[i].replace('"', " ")
		t[i] = t[i].lower()
	f.close()
	return t

def getOccurrenciesVector(doc, motsVides):
	doc = doc.split(" ")
	dico = {}
	for i in doc:
		if(i != ''):
			if(i not in motsVides):
				ps = PorterStemmer()
				i = ps.stem(i)
				if(dico.has_key(i)):
					dico[i] = dico[i]+1
				else:
					dico[i] = 1
	return dico


def cleanQueryVector(query, motsVides):	
	query = query.split(" ")
	cleanedQuery = []
	for i in query:
		if(i != ''):
			if(i not in motsVides):
				ps = PorterStemmer()
				i = ps.stem(i)
				cleanedQuery.append(i)
	return cleanedQuery

def getTermFrenquency(frequencyVector):
	sum = 0
	for i in frequencyVector:  # Recuperation du nombre de mots dans le doc
		sum = sum + frequencyVector[i]
	for i in frequencyVector:  # Calcul du tf pour chaque doc
		t =float(frequencyVector[i])/sum
		frequencyVector[i] = round(t, 4)
	return frequencyVector

def loadMotsVides(file):
	f = open(file, 'r')
	t = f.readlines()
	for i in range(0, len(t)) :
		t[i] = t[i].replace('\n', "")
	return t

def DC(descTable, word ) :
	cpt = 0
	for i in descTable :
		if ( word in i.keys()) :
			cpt+=1
	return cpt

def idf(descTable, tabWord):
	n = len(descTable)
	tmp = {}
	for word in tabWord :
		dc=0
		dc = DC(descTable, word)	
		tmp[word]=math.log10(n/dc)
	return tmp

					
	

def saveDescripteur(tab):
	txt = json.dumps(tab)
	f = open("descripteur.json", "w")
	f.write(txt)
	f.close() 
	

def generateDescripteur(file):
	doc = loadDoc(file)
	motsVide = loadMotsVides("motsvides.txt")
	biblio = []
	for i in range (1, len(doc)):
		vect = getOccurrenciesVector(doc[i], motsVide)
		vect = getTermFrenquency(vect)
		biblio.append(vect)
	saveDescripteur(biblio)
	
	
def loadDescripteur():
	f = open("descripteur.json", "r")
	txt = f.read()
	tab = json.loads(txt)
	return tab

def normeVect(dic):
	norm=0
	for i in dic:
		norm = norm + (dic[i])**2
		norm = math.sqrt(norm)
	return norm


def main():
	
	mode = sys.argv[1]
	
	if(mode == "-load"):
		file = sys.argv[2]
		generateDescripteur(file)
	elif(mode == "-search"):
		request = sys.argv[2]

		##TODO:
		descripteur = loadDescripteur()
		print(idf(descripteur, "familiar"))
	return 0

main()
