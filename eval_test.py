import sys
import getdf
import json


def main():
    """ 2 differents arguements :
            - -load test +query_file_name : Loading the file containing query and put the differents queries into a json
                                            file test_request.json
            - no argument : load and execute n research with the n queries stored on test_request.json
    """
    mode = ""                   # Check if mode is load_test
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == "-load_test":    # Load file and stored queries on the json
        fil = sys.argv[2]
        f = open(fil, "r")
        t = f.read().split(".I")
        for i in range(0, len(t)):  # Clean target file
            t[i] = t[i].replace('.W\n', "")
            t[i] = t[i].replace('\n', " ")
            t[i] = t[i].replace(',', " ")
            t[i] = t[i].replace('.', "")
            t[i] = t[i].replace('"', "")
            t[i] = t[i].lower()
        f.close()
        txt = json.dumps(t)
        jsonFile = open("data/test_request.json", "w")
        jsonFile.write(txt)
        jsonFile.close()

    else:   # Run n research with the n queries stored in test_request.json
        f = open("data/test_request.json", "r")
        txt = f.read()
        req = json.loads(txt)
        for i in range(1, len(req)):
            print ("request n" + str(i))
            print(getdf.search(req[i]))


main()

# TODO ajout calcul rappel preci vitesse(comparer avec la taille de la base)

# ++ embeding de mots/comment representer un doc autrement + distance entre deux documents
