from nltk.stem import PorterStemmer
import json

global motsVide


def getDoc(filename, nb):
	"""Load the file according his id"""
	# f = open(file, "r")
	# t = (f.read().split(".I "))[nb]
	# f.close()
	# t = load_json("data/database.json")[nb]
	t = load_json(filename)[nb]
	return t


def loadDoc(filename):
	"""Open target file and clean up the lines."""
	# t = load_json("data/database.json")
	t = load_json(filename)
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


def load_empty_words(empty_word_list):
	"""Get word on the given list and build a list of them"""
	f = open(empty_word_list, 'r')
	t = f.readlines()
	for i in range(0, len(t)):
		t[i] = t[i].replace('\n', "")
	return t


motsVide=load_empty_words("data/motsvides.txt")

