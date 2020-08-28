from NotInList import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-list", "--listfile")
parser.add_argument("-bed", "--bedfile")
parser.add_argument("-out", "--outputfile")

args = parser.parse_args()


def F_NotInList(listfile, bedfile, outputfile):
    list = []
    with open(listfile, "r") as fp:
        for line in fp:
            div = line.rstrip("\n")
            list.append(div)
    with open(bedfile, "r") as fp, open(outputfile, "w") as fout:
        for line in fp:
            sample_name = line.rstrip("\n").split("\t")[5].rstrip(".rpkm")
            if sample_name not in list:
                fout.write(line)
    return 1


if __name__ == "__main__":
    bedfile = args.bedfile
    listfile = args.listfile
    outputfile = args.outputfile
    F_NotInList(listfile=listfile, bedfile=bedfile, outputfile=outputfile)
else:
    pass
