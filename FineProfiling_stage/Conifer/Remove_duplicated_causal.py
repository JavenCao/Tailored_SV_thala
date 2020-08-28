from Remove_duplicated_causal import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-bed", "--bedfile")
parser.add_argument("-uniqbed", "--uniqbedfile")


args = parser.parse_args()

# chr    pos1    pos2    range   Deletion_with_support_Reads Sample_Name Known_chr   Known_pos1  Known_pos2  HbVar   Common_name HGVS_name   Type    Overlapping(0=completely)


def F_Remove_duplicated_causal(bedfile, uniqbedfile):
    uniq_causal_dict = {}
    with open(bedfile, "r") as fp:
        for line in fp:
            div = line.rstrip("\n").split("\t")
            sample_name = str(div[5])
            Hbvar = str(div[9])
            current_key = sample_name + "_" + Hbvar
            uniq_causal_dict[current_key] = div[5] + "\t" + div[6] + "\t" + div[7] + "\t" + \
                div[8] + "\t" + div[9] + "\t" + div[10] + \
                "\t" + div[11] + "\t" + div[12] + "\n"

    with open(uniqbedfile, "w") as fout:
        for key in uniq_causal_dict.keys():
            fout.write(uniq_causal_dict[key])
    return 1


if __name__ == "__main__":
    bedfile = args.bedfile
    uniqbedfile = args.uniqbedfile
    F_Remove_duplicated_causal(bedfile, uniqbedfile)

else:
    pass
