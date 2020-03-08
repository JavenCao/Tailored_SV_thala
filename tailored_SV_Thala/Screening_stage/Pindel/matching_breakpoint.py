from matching_breakpoint import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-knownbed", "--knownbedfile")
parser.add_argument("-bed", "--bedfile")
parser.add_argument("-outbed", "--outbedfile")
args = parser.parse_args()


def F_mathcing_breakpoint(knownbedfile, bedfile, outbedfile):
    db_dict = {}
    with open(knownbedfile, "rb") as fp:
        for line in fp:
            div = line.rstrip("\n").split("\t")
            Chr = div[0]
            Pos1 = str(div[1])
            Pos2 = str(div[2])
            key = Chr + "_" + Pos1 + "_" + Pos2
            value = line.rstrip("\n")
            db_dict[key] = value

    with open(bedfile, "rb") as fp, open(outbedfile, "w") as fout:
        i = 1
        for line in fp:
            if i == 1:
                i = 2
            else:
                div = line.rstrip("\n").split("\t")
                current_Chr = div[0]
                current_Pos1 = int(div[1])
                current_Pos2 = int(div[2])
                for key in db_dict.keys():
                    db_chr = key.split("_")[0]
                    db_pos1 = int(key.split("_")[1])
                    db_pos2 = int(key.split("_")[2])
                    if (current_Chr == db_chr) and (current_Pos1 >= db_pos1 - 10) and (current_Pos1 <= db_pos1 + 10) and (current_Pos2 >= db_pos2 - 10) and (current_Pos2 <= db_pos2 + 10):
                        newline = line.rstrip(
                            "\n") + "\t" + db_dict[key] + "\n"
                        fout.write(newline)
    return 1


if __name__ == "__main__":
    knownbedfile = args.knownbedfile
    bedfile = args.bedfile
    outbedfile = args.outbedfile
    F_mathcing_breakpoint(knownbedfile=knownbedfile,
                          bedfile=bedfile, outbedfile=outbedfile)
else:
    pass
