from nltk.stem import PorterStemer
 

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
		ps = PorterStemer()
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


def main():
	doc = loadDoc()
	motsVide = loadMotsVides("motsvides.txt")
	vect = getFrenquencyVector(doc[1], motsVide)
	print(vect)
	print
	print(getFrenquencyVector(doc[1], []))
	return 0


main()
