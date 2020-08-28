import os
from SV_scripts import *

if __name__ == "__main__":
    Path_dict = {}
    SampleList = []

    # load values from config file
    Path_dict, SampleList = load_config_file("SV_configure_file.txt")

    SV_folder = Path_dict.get("SV_folder")
    Screening_stage_F = SV_folder.rstrip('/') + '/' + "Screening_stage"
    each_software_F = ['Conifer', 'Pindel', 'BreakDancer']

    Create_Folders(Screening_stage_F, each_software_F)

    Conider_scripts_folder = os.getcwd() + '/Screening_stage/Conifer'
    FP_Conider_scripts_folder = os.getcwd() + '/FineProfiling_stage/Conifer'
    Pindel_scripts_folder = os.getcwd() + '/Screening_stage/Pindel'
    BreakDancer_scripts_folder = os.getcwd() + '/Screening_stage/BreakDancer'

# create Conifer scripts
    Conifer_Folder = Screening_stage_F + '/Conifer'
    Conifer_RPKM_Folder = Screening_stage_F + '/Conifer/RPKM'
    os.mkdir(Conifer_RPKM_Folder)
    Conifer_RPKM_Modelfile = Conider_scripts_folder + '/step0_rpkm_model.pbs'

    ModifyAndCreate_v2(Conifer_RPKM_Modelfile, Path_dict,
                       Conifer_Folder, SampleList, "RPKM_cal")

    Conifer_Run_Modelfile = Conider_scripts_folder + '/step1_main_run_Conifer.pbs'
    ModifyAndCreate_v2(Conifer_Run_Modelfile, Path_dict,
                       Conifer_Folder, SampleList, "Conifer_Run")

# create BreakDancer scripts
    BreakDancer_Folder = Screening_stage_F + '/BreakDancer'
    BreakDancer_Modefile = BreakDancer_scripts_folder + '/run_BreakDancer.pbs'
    ModifyAndCreate_v2(BreakDancer_Modefile, Path_dict,
                       BreakDancer_Folder, SampleList, "BreakDancer_Run")

# create Pindel scripts
    Pindel_Folder = Screening_stage_F + '/Pindel'
    Pindel_Modefile = Pindel_scripts_folder + '/run_Pindel.pbs'
    ModifyAndCreate_v2(Pindel_Modefile, Path_dict,
                       Pindel_Folder, SampleList, "Pindel_Run")

# 2020new - fine profiling stage
    FineProfiling_stage_F = SV_folder.rstrip('/') + '/' + "FineProfiling_stage"
    each_software_F = ['Conifer']
    Create_Folders(FineProfiling_stage_F, each_software_F)
#   FP_Conider_scripts_folder = os.getcwd() + '/FineProfiling_stage/Conifer'
    Conifer_Run_Modelfile = FP_Conider_scripts_folder + \
        '/FP_step1_main_run_Conifer.pbs'
    SV_folder = Path_dict.get("SV_folder")
    FineProfiling_stage_F_conifer = SV_folder.rstrip(
        '/') + '/' + "FineProfiling_stage/Conifer"
    ModifyAndCreate_v2(Conifer_Run_Modelfile, Path_dict,
                       FineProfiling_stage_F_conifer, SampleList, "Conifer_Run")

    Fine_profiling_list_modelfile = FP_Conider_scripts_folder + "/Fine_profiling_list.pbs"
    ModifyAndCreate_v2(Fine_profiling_list_modelfile, Path_dict,
                       FineProfiling_stage_F_conifer, SampleList, "Fine_profiling_list")

else:
    pass


def load_config_file(config_name):
    """ load parameters from a config file"""
    config_var = ['SV_folder', 'Raw_Bam_file_folder', 'samtools_path',
                  'CONIFER_path', 'BREAKDANCER_path', 'PINDEL_path', 'Bam_file_reference', 'queue', 'walltime', 'nodes', 'ppn', 'mem', 'Email']

    config_dict = {}

    SampleList = []

    with open(config_name) as ConfigFile:
        for line in ConfigFile:
            line = line.rstrip('\n')
            # Sample lines
            if(line.startswith("sample")):
                SampleInfo = line.split('=')
                SampleList.append(SampleInfo[1])
            else:
                info = line.split('=')
                if(info[0]) in config_var:
                    config_dict[info[0]] = info[1]

    return config_dict, SampleList


def Create_Folders(OuterSide, InnerListNames):
    """First create OuterSide folder, then Within the OuterSide, create each Inner folder in the order of InnerListNanes"""
    try:
        os.mkdir(OuterSide)
        for i in InnerListNames:
            subfolder = OuterSide + '/' + i
            os.mkdir(subfolder)
    except OSError:
        print """
        |-----------------------------------------------------|
        | Please delete all the newly created Screening_stage |
        | folders and re-run this script again !              |
        |-----------------------------------------------------|
        """
    return 1


def ModifyAndCreate_v2(modelfile, Path_dict, TargetFolder, SampleList, prefix):
    """under each sample folder, create its own PBS files, with name prefix_sample.pbs"""
    with open(modelfile) as file:
        l = file.readlines()
        for i in range(len(l)):
            # Set the job name
            if(l[i].startswith("#PBS -N")):
                l[i] = "#PBS -N " + prefix + '\n'

            elif(l[i].startswith("#PBS -l")):
                l[i] = """#PBS -l mem={0},nodes={1}:ppn={2},walltime={3}{4}""".format(Path_dict.get(
                    'mem'), Path_dict.get('nodes'), Path_dict.get('ppn'), Path_dict.get('walltime'), '\n')

            elif(l[i].startswith("#PBS -q")):
                l[i] = """#PBS -q {0}{1}""".format(
                    Path_dict.get('queue'), '\n')

            elif(l[i].startswith("#PBS -m abe -M")):
                l[i] = "#PBS -m abe -M " + Path_dict.get('Email') + '\n'

            elif(l[i].startswith("SV_folder")):
                l[i] = "SV_folder=" + Path_dict.get('SV_folder') + '\n'

            elif(l[i].startswith("Raw_Bam_file_folder")):
                l[i] = "Raw_Bam_file_folder=" + \
                    Path_dict.get('Raw_Bam_file_folder') + '\n'

            elif(l[i].startswith("GATK_Bundle")):
                l[i] = "GATK_Bundle=" + \
                    Path_dict.get("GATK_bundle_path") + '\n'

            elif(l[i].startswith("BWA")):
                l[i] = "BWA=" + Path_dict.get("BWA_path") + '\n'

            elif(l[i].startswith("SAMTOOLS")):
                l[i] = "SAMTOOLS=" + Path_dict.get("samtools_path") + '\n'

            elif(l[i].startswith("PICARD")):
                l[i] = "PICARD=" + Path_dict.get("picard_path") + '\n'

            elif(l[i].startswith("GATK")):
                l[i] = "GATK=" + Path_dict.get("GATK_path") + '\n'

            elif(l[i].startswith("ANNO")):
                l[i] = "ANNO=" + Path_dict.get("ANNO_path") + '\n'

            elif(l[i].startswith("CONIFER")):
                l[i] = "CONIFER=" + Path_dict.get("CONIFER_path") + '\n'

            elif(l[i].startswith("PINDEL=")):
                l[i] = "PINDEL=" + Path_dict.get("PINDEL_path") + '\n'

            elif(l[i].startswith("REFSEQ")):
                l[i] = "REFSEQ=" + Path_dict.get("Bam_file_reference") + '\n'

            elif(l[i].startswith("BREAKDANCER")):
                l[i] = "BREAKDANCER=" + \
                    Path_dict.get("BREAKDANCER_path") + '\n'

            elif(l[i].startswith("for i in all_samples")):
                l[i] = None
                t = ''
                for sample in SampleList:
                    t = t + sample + ' '
                newline = "for i in " + t + '\n'
                l[i] = newline

    newFileName = TargetFolder + '/' + prefix + '.pbs'
    with open(newFileName, 'wt') as newFile:
        newFile.writelines(l)
    return 1
