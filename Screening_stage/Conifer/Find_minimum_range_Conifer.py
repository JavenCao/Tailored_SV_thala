from Find_minimum_range_Conifer import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-bed", "--bedfile")
parser.add_argument("-minbed", "--minbedfile")
args = parser.parse_args()


def Find_minimum_range_fun(bedfile, minbedfile):
    """input is from bedtools closest"""
    with open(bedfile, "r") as fp:
        All_lines = fp.readlines()
        D_min_line_value = {}
        D_min_line_index = {}
# initial the two dict
        ini_line = All_lines[0]
        div = ini_line.rstrip("\n").split("\t")
        d1 = abs(int(div[1]) - int(div[7]))
        d2 = abs(int(div[2]) - int(div[8]))
        D_current_line_key = div[0] + "\t" + \
            str(div[1]) + "\t" + str(div[3]) + "\t" + str(div[5])
        D_current_line_value = d1 + d2
        D_current_line_index = 0
        D_min_line_value[D_current_line_key] = D_current_line_value
        D_min_line_index[D_current_line_key] = D_current_line_index

        for i in range(1, len(All_lines)):
            div = All_lines[i].rstrip("\n").split("\t")
            d1 = abs(int(div[1]) - int(div[7]))
            d2 = abs(int(div[2]) - int(div[8]))
            D_current_line_key = div[0] + "\t" + \
                str(div[1]) + "\t" + str(div[3]) + "\t" + str(div[5])
            D_current_line_value = d1 + d2
            if D_current_line_key in D_min_line_value.keys():
                if D_current_line_value < D_min_line_value[D_current_line_key]:
                    D_min_line_value[D_current_line_key] = D_current_line_value
                    D_min_line_index[D_current_line_key] = i
            else:
                D_min_line_index[D_current_line_key] = i
                D_min_line_value[D_current_line_key] = D_current_line_value
# output
    out_put_line_index_list = D_min_line_index.values()
    headerLine = "chr\tpos1\tpos2\trange\tDeletion_with_support_Reads\tSample_Name\tKnown_chr\tKnown_pos1\tKnown_pos2\tHbVar\tCommon_name\tHGVS_name\tType\tOverlapping(0=completely)\n"
    with open(minbedfile, "w") as fout:
        fout.write(headerLine)
        for out_put_line_index in out_put_line_index_list:
            line = All_lines[out_put_line_index]
            div = line.rstrip("\n").split("\t")
#            fout.write(line)
            if abs(int(div[3]) - (int(div[8]) - int(div[7]))) < 2000 and (int(div[8]) - int(div[7])) > 1000:
                fout.write(line)
    return 1


if __name__ == "__main__":
    bedfile = args.bedfile
    minbedfile = args.minbedfile
    Find_minimum_range_fun(bedfile, minbedfile)
else:
    pass
