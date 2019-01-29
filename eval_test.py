from time import sleep

import getdf
import json


def is_in(liste, element):
    b = False
    for i in liste:
        if str(element) == str(i):
            b = True
    return b


def main():
    # Get dictonary of relations between query and documents
    jsonfile= open("data/relations.json")
    jsonstr = jsonfile.read()
    rel = json.loads(jsonstr)

    # Run n research with the n queries stored in test_request.json
    f = open("data/request.json", "r")
    txt = f.read()
    req = json.loads(txt)
    for i in range(1, len(req)):
        print ("request n" + str(i) + ":" + str(req[i]))
        if rel.has_key(str(i)):
            rep_ex = getdf.sortResult(getdf.search(req[i]))
            rep_th = rel[str(i)]
            rep_ex_doc = []
            for j in range(len(rep_th)):
                rep_ex_doc.append(rep_ex[j][0])
            # rep_ex_doc
            # rep_th
            some = 0
            for j in range(len(rep_th)):
                if is_in(rep_th, rep_ex_doc[j]):
                    some = some+1
            print (str(some) + "/" + str(len(rep_th)))
            sleep(1)


main()

# TODO ajout calcul rappel preci vitesse(comparer avec la taille de la base)

# ++ embeding de mots/comment representer un doc autrement + distance entre deux documents
