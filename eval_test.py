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
    jsonfile = open("data/relations.json")
    jsonstr = jsonfile.read()
    rel = json.loads(jsonstr)

    # Run n research with the n queries stored in test_request.json
    f = open("data/request.json", "r")
    txt = f.read()
    req = json.loads(txt)
    precision = []
    rappel = []
    for i in range(1, len(req)):
        print ("request n" + str(i) + ":" + str(req[i]))
        if rel.has_key(str(i)):
            rep_ex = getdf.sortResult(getdf.search(req[i]))
            rep_th = rel[str(i)]
            rep_ex_doc = []
            for j in range(len(rep_th)):
                rep_ex_doc.append(rep_ex[j][0])
            # print rep_ex_doc
            # print rep_th
            s = 0
            for j in range(len(rep_th)):
                if is_in(rep_th, rep_ex_doc[j]):
                    s = s+1
            print (str(s) + "/" + str(len(rep_th)))
            precision.append(float(s)/float(len(rep_ex_doc)))
            rappel.append(float(s)/float(len(rep_th)))
    # Calcul precision et rappel
    acc_pre = 0
    for k in precision:
        acc_pre = acc_pre + k
    acc_pre = acc_pre/len(precision)
    print ("precision : " + str(acc_pre))
    acc_rap = 0
    for k in rappel:
        acc_rap = acc_rap + k
    acc_rap = acc_rap/len(rappel)
    print ("rappel : " + str(acc_rap))


main()

# TODO ajout calcul rappel preci vitesse(comparer avec la taille de la base)

# ++ embeding de mots/comment representer un doc autrement + distance entre deux documents
