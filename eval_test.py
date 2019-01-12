import sys
import getdf

def main():

    mode = sys.argv[1]
    motsVide = loadMotsVides("motsvides.txt")

    if mode == "-load":
        file = sys.argv[2]
        generateDescripteur(file, motsVide)

main()

