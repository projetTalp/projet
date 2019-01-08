from nltk.stem import PorterStemmer

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
	
def getFrenquencyVector(doc, motsVides):
	
	doc = doc.split(" ")
	dico = {}
	for i in doc:
		ps = PorterStemmer()
		i = ps.stem(i)
		if(i != ''):
			if(i not in motsVides):
				if(dico.has_key(i)):
					dico[i] = dico[i]+1
				else:
					dico[i] = 1
	return dico

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

def idf(descTable, word):
	dc=0
	dc = DC(descTable, word)
	n = len(descTable)
	print ("taille = ", n, "\n")
	return math.log10(n/dc)
					
	

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
		vect = getFrenquencyVector(doc[i], motsVide)
		biblio.append(vect)
	saveDescripteur(biblio)
	
	
def loadDescripteur():
	f = open("descripteur.json", "r")
	txt = f.read()
	tab = json.loads(txt)
	return tab


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

	#generateDescripteur("firstdata")
	#descripteurs = loadDescripteur()
	#print(descripteurs)
	return 0

main()
