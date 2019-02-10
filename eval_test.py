import json
import argparse
import operator
import time
import getdf
import word2Vec as wv
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
        temps = []
        for i in range(1, len(req)):
            print ("request n" + str(i) + ":" + str(req[i]))
            if rel.has_key(str(i)):
                h = time.time()
                rep_ex = getdf.sortResult(getdf.search(req[i]))
                h = time.time() - h
                rep_th = rel[str(i)]
                rep_ex_doc = []
                temps.append(h)
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
        tps_moyen = 0
        for i in temps:
            tps_moyen = i + tps_moyen
        tps_moyen = tps_moyen / len(temps)
        print ("Temps moyen : " + str(tps_moyen))

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
                    elm = max(dico.iteritems(), key=operator.itemgetter(1))[0]
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
        temps = []
        for i in range(1, len(req)):
            print ("request n" + str(i) + ":" + str(req[i]))
            if rel.has_key(str(i)):
                h = time.time()
                rep_ex = getdf.sortResult(getdf.search_tf(req[i]))
                h = time.time() -h
                temps.append(h)
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
        tps_moyen = 0
        for i in temps:
            tps_moyen = i + tps_moyen
        tps_moyen = tps_moyen / len(temps)
        print ("Temps moyen : " + str(tps_moyen))

    elif mode == "embedding":
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
        temps = []
        for i in range(1, len(req)):
            print ("request n" + str(i) + ":" + str(req[i]))
            if rel.has_key(str(i)):
                h = time.time()
                rep_ex = wv.get_results(req[i])
                h = time.time() - h
                temps.append(h)
                rep_th = rel[str(i)]
                rep_ex_doc = []
                for j in range(len(rep_th)):
                    rep_ex_doc.append(rep_ex[j][0])
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
        tps_moyen = 0
        for i in temps:
            tps_moyen = i + tps_moyen
        tps_moyen = tps_moyen / len(temps)
        print ("Temps moyen : " + str(tps_moyen))

    elif mode == "comparison":
        # Run n research with the n queries stored in test_request.json
        f = open("data/request.json", "r")
        txt = f.read()
        req = json.loads(txt)
        precision = []
        rappel = []
        for i in range(1, len(req)):
            print ("request n" + str(i) + ":" + str(req[i]))
            rep_ex = getdf.sortResult(getdf.search(req[i]))
            rep_ex2 = wv.get_results(req[i])
            rep_ex_doc1 = []
            rep_ex_doc2 = []
            for j in range(0, 10):
                rep_ex_doc1.append(rep_ex[j][0])
                rep_ex_doc2.append(rep_ex2[j][0])
            s = 0
            for j in range(len(rep_ex_doc1)):
                if is_in(rep_ex_doc1, rep_ex_doc2[j]):
                    s = s+1
            print (str(s) + "/" + str(len(rep_ex_doc1)))
            precision.append(float(s)/float(len(rep_ex_doc1)))
            rappel.append(float(s)/float(len(rep_ex_doc2)))
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

    else:
        print("Incorect mode")
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update or creation of differents json file")
    parser.add_argument('-m', "--mode", required=True, help="Select one of : random, tf, tfid, embedding")
    args = parser.parse_args()
    main(args.mode)


