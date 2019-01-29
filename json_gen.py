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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update or creation of differents json file")
    parser.add_argument("--mode", required=True, help="Select one of : query/tfidf")
    parser.add_argument("--filename", required=True, help="name of the target file")
    args = parser.parse_args()
    main(args.mode, args.filename)


