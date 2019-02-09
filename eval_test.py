from time import sleep
import argparse
import operator

import getdf
import json

""" Script for evaluate the queries given by CISI with his documents and compare results with theorical results"""


def is_in(liste, element):
    """Check if an element is on a list"""
    for i in liste:
        if str(element) == str(i):
            return True
    return False


def main(mode):
    """Calcul precision / rappel / F-score for a selection mode"""
    if mode == "tfidf":
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
        print ("F-score :" + str(acc_rap*acc_pre*2/(acc_rap+acc_pre)))

    elif mode == "random":
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
                rep_th = rel[str(i)]
                rep_ex_doc = []
                dico = getdf.get_sim_random()
                for j in range(len(rep_th)):
                    elm =max(dico.iteritems(), key=operator.itemgetter(1))[0]
                    rep_ex_doc.append(elm)
                    dico.pop(elm, None)
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
        print ("F-score :" + str(acc_rap*acc_pre*2/(acc_rap+acc_pre)))

    elif mode == "tf":
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
                rep_ex = getdf.sortResult(getdf.search_tf(req[i]))
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
        print ("F-score :" + str(acc_rap*acc_pre*2/(acc_rap+acc_pre)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update or creation of differents json file")
    parser.add_argument('-m', "--mode", required=True, help="Select one of : random, tf, tfid, embedding")
    args = parser.parse_args()
    main(args.mode)



# TODO : Bien appuyer sur les differents test : montrer train / tests, donner les chiffres.

# TODO : Embedding et (neuronnes)

# TODO : Ameliorer le temps : liste inversee par exemple, garder les json en memoire
