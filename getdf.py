from nltk.stem import PorterStemmer
import math

def loadDoc():
	f = open("firstdata", "r")
	t = f.read().split(".I ")
	for i in range(0, len(t)) :
		t[i] = t[i].replace('\n', " ")
		t[i] = t[i].replace(',', " , ")
		t[i] = t[i].replace('.', " . ")
		t[i] = t[i].lower()
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
	return math.log10(n/dc)
					
	

def main():
	doc = loadDoc()
	motsVide = loadMotsVides("motsvides.txt")
	vect = getFrenquencyVector(doc[1], motsVide)
	print(vect)
	print
	print(getFrenquencyVector(doc[1], []))
	return 0


main()
