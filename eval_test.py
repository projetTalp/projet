import sys
import getdf
import json


def main():

    mode = ""
    if len(sys.argv) > 1:
        mode = sys.argv[1]


    if mode == "-load_test":
        file = sys.argv[2]
        f = open(file, "r")
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
        jsonFile = open("test_request.json", "w")
        jsonFile.write(txt)
        jsonFile.close()

    else:
        f = open("test_request.json", "r")
        txt = f.read()
        req = json.loads(txt)
        for i in req:
            getdf.search(i)

main()

