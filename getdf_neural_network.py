from keras.models import load_model
import trt_doc as td
import getdf as gt

# coding=<utf-8>

global model, indice_key
model = load_model('Reseau_de_neurone/my_model.json')

def getIndiceKey():
	dico = td.load_json("./data/idf.json")
	d = {}
	i = 0
	for word in dico.keys():
		d[word] = i
		i = i+1
	return d
	
indice_key = getIndiceKey() ## TODO: load depuis un json !!! /!\ Depend de la base selectionne


def search(request):
	"""			"""
	vectRequestIDF = getTFIdfResquest(request)
	mots = vectRequestIDF.keys()
	tab = {}
	for i in mots:
		for doc in gt.liste_inverse[i]:
			tab[doc] = True
	result = findSimilarite(vectRequestIDF, tab)
	return result


def getTFIdfResquest(req):
	req = td.cleanup(req)
	tmp = gt.getOccurrenciesVector(req, gt.motsVide)
	tf = gt.getTermFrenquency(tmp)
	tf_idf = {}
	for word in tf:
		if gt.idf.has_key(word):
			tf_idf[word] = tf[word] * gt.idf[word]
	return tf_idf
	


def findSimilarite(vectRequestIDF, id_descripteur):
	## Utilisation du reseau de neuronne pour predire le resulat 
	result = {}
	tab_req = dicoToTab(vectRequestIDF)
	for vectDesc in id_descripteur:
		tab_desc = dicoToTab(gt.descripteurs[vectDesc-1])
		big_tab = tab_desc + tab_req
		print(len(big_tab))
		result[vectDesc] = model.predict(big_tab)
		print (result[vectDesc])
	return result


def dicoToTab(dico):
	tab = []
	for word in indice_key:
		if dico.has_key(word):
			tab.append(dico[word])
		else:
			tab.append(0)
	return tab


