import argparse
import json

import getdf


def main(mode, filename):

    if mode == "query":  # Generate the json containing different queries
        f = open(filename, "r")
        t = f.read().split(".I")
        for i in range(0, len(t)):  # Clean target file
            t[i] = t[i].replace('.W\n', "")
            t[i] = t[i].replace('\n', " ")
            t[i] = t[i].replace(',', " ")
            t[i] = t[i].replace('.', "")
            t[i] = t[i].replace('"', "")
            t[i] = t[i].lower()
        txt = json.dumps(t)
        f.close()
        jsonFile = open("data/request.json", "w")
        jsonFile.write(txt)
        jsonFile.close()

    elif mode == "tfidf":
        print("TF Generation")
        getdf.generateTF(filename)
        print("IDF Generation")
        getdf.generateIDF(filename)
        print("TFIDF Generation")
        getdf.getTfIdfVector()

    elif mode == "relations":
        rel = {}  # Creation of the relation dictionnary
        f = open(filename, "r")
        data = f.readlines()
        for line in data:  # Get a relation and store it to the dictionnary
            elements = line.split()
            doc = elements[0]
            query = elements[1]
            if not rel.has_key(doc):
                rel[doc] = []
            rel[doc].append(query)
        getdf.save_json(rel, "data/relations.json")

    elif mode == "database":
        f = open(filename, "r")
        t = f.read().split(".I ")
        for i in range(0, len(t)):  # Clean target file
            a = t[i].split('\n')
            text = ""
            for z in range(1, len(a)):
                text = text + " " + a[z]
                t[i] = text
        f.close()
        getdf.save_json(t, "data/database.json")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update or creation of differents json file")
    parser.add_argument("--mode", required=True, help="Select one of : query/tfidf/relations/database")
    parser.add_argument("--filename", required=True, help="name of the target file")
    args = parser.parse_args()
    main(args.mode, args.filename)


