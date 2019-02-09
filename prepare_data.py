import time
import getdf
import trt_doc as td
import random


def getIndiceKey():
	dico = td.load_json("./data/idf.json")
	d = {}
	i = 0
	for word in dico.keys():
		d[word] = i
		i = i+1
	return d
	
	
def is_in(liste, element):
    for i in liste:
        if str(element) == str(i):
            return True
    return False

def prepareData():
	print("debut de la preparation des donnees...")
	print("chargement des json...")
	result = td.load_json("./data/relations.json")
	tfidf = td.load_json("./data/tfidf.json")
	req = td.load_json("./data/request.json")
	print("creation de la base de mots")
	indice_key = getIndiceKey()
	
	
	
	## Trop de donnee pour faire comme ca... 
	#for numReq in result:
	#	numReq = int(numReq)
	#	tfidf_req = getdf.getTFIdfResquest(req[numReq])
	#	tab_req = dicoToTab(tfidf_req, indice_key)
		
		
		#for i in range(0, len(tfidf)):
		#	tfidf_doc = tfidf[i]
		#	tab_doc = dicoToTab(tfidf_doc, indice_key)
		#	data = tab_doc + tab_req
		#	if is_in(result, i+1): #decalage; ERREUR !!! 
		#		data.append(1) ##la requete match avec le doc
		#	else:
		#		data.append(0) ##la requete match pas avec le doc
		#	datas.append(data)
		
	## Methode 2 : ajouter les n doc qui match + n doc random qui match pas + ecriture de tps en tps pour pas saturer la memoire
	
	print("encodage de tfidf...")
	#print(result)
	tfidf_encode = []
	for i in tfidf:
		tfidf_encode.append(encode_csv(dicoToTab(i, indice_key)))
		
	print("lancement de la generation...")
	datas = ""
	for numReq in result:
		#numReq = int(numReq)
		tfidf_req = getdf.getTFIdfResquest(req[int(numReq)]) 
		req_encode = encode_csv(dicoToTab(tfidf_req, indice_key))
		
		n = len(result[numReq])
		docs = {}
		for i in range(0, n-1):
			doc = int(result[numReq][i])-1
			docs[doc] = True
			ligne = tfidf_encode[doc] + req_encode + "1\n"
			datas = datas + ligne
		
		## rajouter n mauvaise correspondance en aleatoire
		c = 0
		while c < n:
			rand = random.randrange(0, len(tfidf), 1)
			if not docs.has_key(rand):
				c = c + 1
				ligne = tfidf_encode[rand] + req_encode + "0\n"
				datas = datas + ligne
				
		print("donnes de la requete: "+numReq)
		##print(datas)
		
	#time.sleep(10)
	#s = encode_csv(datas)
	saveDatas(datas)
	
def dicoToTab(dico, indiceKey):
	tab = []
	for word in indiceKey:
		if dico.has_key(word):
			tab.append(dico[word])
		else:
			tab.append(0)
	return tab
	
	
#def encode_csv(tab):
#	s = ""
#	firstData = True
#	for data in tab:
#		if firstData:
#			firstData = False
#		else:
#			s = s + "\n"
#		firstVal = True
#		for val in data:	
#			if firstVal:
#				firstVal = False
#				##print(s)
#			else:
#				s = s + ";"
#			s = s + str(val)#
#	return s
	

def encode_csv(tab):
	s = ""
	for data in tab:
		s = s + str(data) + ";" 
	return s
	
def saveDatas(s):
	f = open("Reseau_de_neurone/data_moteur_recherche.csv", "w")
	f.write(s)
	f.close()	
		

def splitTrainDevTest(fileInput):
	train_file = "Reseau_de_neurone/data_train.csv"
	dev_file = "Reseau_de_neurone/data_dev.csv"
	test_file = "Reseau_de_neurone/data_test.csv"

	train = 0.6
	dev = 0.2
	test = 0.2
	
	f = open(fileInput, "r")
	lignes = f.readlines()
	N = len(lignes)
	n1 = int(train * N)
	n2 = int(dev * N)
	n3 = int(test * N)
	
	t1 = ""
	t2 = ""
	t3 = ""
	print("generation")
	for i in range(0, n1):
		t1 = t1 + lignes[i] + "\n"
	print("ecriture f1")
	f1 = open(train_file, "w")
	f1.write(t1)
	f1.close()
	
	print("generation")
	for i in range(n1+1, n1+n2):
		t2 = t2 + lignes[i] + "\n"
	print("ecriture f2")
	f2 = open(dev_file, "w")
	f2.write(t2)
	f2.close()
	
	print("generation")
	for i in range(n1+n2+1, n1+n2+n3):
		t3 = t3 + lignes[i] + "\n"
	print("ecriture f3")
	f3 = open(test_file, "w")
	f3.write(t3)
	f3.close()
	
## prepareData()


## Melanger le fichier en cmd dans le terminal :
	##perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < Reseau_de_neurone/data_moteur_recherche.csv > data_shuffle.csv

## splitTrainDevTest("Reseau_de_neurone/data_shuffle.csv")

txt = "0"
for i in range(1, 13214):
	txt = txt + "," + str(i)
print (txt)



"""
#tab = [[1, 0 ,0.5, 4, 6], [0.4, 6, 4, 8, 2], [4, 2, 6, 0.3, 0], [0, 0, 4, 5, 3]] 
#print(encode_csv(tab))
f = open("Reseau_de_neurone/data_moteur_recherche (autre copie).csv", "r")
l = f.readlines()
un = 0
zero = 0
for ligne in l:
	t = ligne.split(';')
	N = len(t) - 1
	if int(t[N]) == 1:
		un = un + 1
	elif int(t[N]) == 0:
		zero = zero + 1 
print("zero = " + str(zero))
print("un = " + str(un))
"""
