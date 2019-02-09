import argparse
import json
import trt_doc as td

import getdf


def loadBaseFileProf(filename):
	"""Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems."""
	f = open(filename, "r")
	t = f.read().split(".I ")
	c = 0 
	for i in range(0, len(t)):  # Clean target file
		a = t[i].split('\n')
		text = ""
		for z in range(1, len(a)):
			text = text + " " + a[z]
		if text != "":
			t[c] = text
			c = c+1
	f.close()
	td.save_json(t, filename + ".json")


"""
def loadBaseCSV(filename):
	Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems.
	f = open(filename, "r")
	t = f.read().split("\n")
	f.close()
	return t
"""


def loadBaseNYT(filename):
	"""Open target file and split it according to the differents lines .I.
Then, replace some character to avoid problems."""
	f = open(filename, "r")
	t = f.read().split("URL:")
	c = 0
	for i in range(0, len(t)):  # Clean target file
		a = t[i].split('\n')
		text = ""
		for z in range(1, len(a)):
			text = text + " " + a[z]
		if text != "":
			t[c] = text
			c = c+1
	f.close()
	td.save_json(t, "data/NYT.json")


def generate_JSON_DataBase(filenames):
	database = []
	for filename in filenames :
		js = td.load_json(filename)
		database = database + js
	td.save_json(database, "data/database.json")


def main(mode, filename):
	if mode == "query":  # Generate the json containing different queries
		f = open("data/CISI.QRY", "r")
		t = f.read().split(".I")
		for i in range(0, len(t)):  # Clean target file
			a = t[i].split('\n')
			text = ""
			for z in range(2, len(a)):
				text = text + " " + a[z]
			t[i] = td.cleanup(text)
		txt = json.dumps(t)
		f.close()
		jsonFile = open("data/request.json", "w")
		jsonFile.write(txt)
		jsonFile.close()

	elif mode == "tfidf":
		print("TF Generation")
		getdf.generateTF("data/database.json")
		print("IDF Generation")
		getdf.generateIDF("data/database.json")
		print("TFIDF Generation")
		getdf.getTfIdfVector()

	elif mode == "relations":  # For test
		rel = {}  # Creation of the relation dictionnary
		f = open("data/CISI.REL", "r")
		data = f.readlines()
		for line in data:  # Get a relation and store it to the dictionnary
			elements = line.split()
			doc = elements[0]
			query = elements[1]
			if not rel.has_key(doc):
				rel[doc] = []
			rel[doc].append(query)
		td.save_json(rel, "data/relations.json")

	elif mode == "database":
		generate_JSON_DataBase(filename)
		
	elif mode == "load-NYT":
		loadBaseNYT(filename[0])
		
	elif mode == "load-BaseProf":
		loadBaseFileProf(filename[0])

	elif mode == "liste_inverse":
		return 0


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Update or creation of differents json file")
	parser.add_argument('-m', "--mode", required=True, help="Select one of : query/tfidf/relations/database/load-NYT/load-BaseProf")
	parser.add_argument('-fn', "--filename", nargs='+', required=False, help="if needed, the different source files")
	args = parser.parse_args()
	main(args.mode, args.filename)
