import sys
from time import sleep

import getdf
import json


def main():
    # Run n research with the n queries stored in test_request.json
    f = open("data/test_request.json", "r")
    txt = f.read()
    req = json.loads(txt)
    for i in range(1, len(req)):
        print ("request n" + str(i) + ":" + str(req[i]))
        print(getdf.sortResult(getdf.search(req[i])))
        sleep(30)


main()

# TODO ajout calcul rappel preci vitesse(comparer avec la taille de la base)

# ++ embeding de mots/comment representer un doc autrement + distance entre deux documents
