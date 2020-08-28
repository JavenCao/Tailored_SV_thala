# tailored_SV_thala

This repository describes the general workflow for thalassaemia structural variation(SV) detection. Common thalassaemia SV includes deletions and du(tri)plications, such as South East Type deletion(--SEA), alpha-3.7kb deletion(-a3.7) and alpha-4.2kb deletion(-a4.2), depending on the local epidemiology. Also, compound rearrangments, such as --SEA/a3.7 can happen and cause Hb H disease.

Here, we want to emphasize that the input alignment BAM files should **not** go through re-align process in point mutation/Indel detection paradigm. If you start with a large BAM file from whole genome sequencing, you are suggested to extract BAM records within the hemoglobin regions to accelerate the calling process, and perhapes the command likes:

    samtools view -h -L Thalassaemia_hg19_genome.bed -b -o output.bam input.bam

Also, make sure that your BAM files are organised by the following structure. In short, each BAM file locates in each sample's folder:

        | -- Bam_file_folder
        |   | -- Sample1
        |   |   | -- Sample1.bam
        |   | -- Thala_2
        |   |   | -- Thala_2.bam
        |   | -- TJLE
        |   |   | -- TJLE.bam

To detect thalassaemia SVs, the selected software [BreakDancer](https://github.com/genome/breakdancer), [Pindel](https://github.com/genome/pindel) and [Conifer](http://conifer.sourceforge.net/) were jointly used with tailored parameters. More details about the parameter settings and considerations can be found in the [original paper](blank).

Besides, a two-stage strategy is used to further confirm and detect the compound CNV status in HBA genes:

In the first **screening stage**, all the samples will be tested together by the three software. Then, samples with deletions covering both the HBA2 and HBA1 genes will be labeled as Group I, while others are labeled as Group II.

In the next **fine profiling stage**, CNV status will be tested by Conifer within each group before the interpretation of the mutation.

bedtools should be in your environments

## Step-by-step description for thalassaemia SV detection

This working example help users to generate structured folder layers and PBS scripts for job submission. However, these PBS files can also be run by bash(sh) on servers that are PBS-free.

* Step1: install the forementioned software, [BreakDancer](https://github.com/genome/breakdancer), [Pindel](https://github.com/genome/pindel) and [Conifer](http://conifer.sourceforge.net/).

* Step2: download this repository to the working directory(such as /home/data/Thala/SV/)by running the follwing commands:

      cd /home/data/Thala/SV/
      git clone https://github.com/JavenCao/Tailored_SV_thala.git

You will need the [Anaconda](https://docs.conda.io/en/latest/) for Python package manager for Conifer:

    cd ./Tailored_SV_thala/
    conda env create --file environment.yml

* Step3: set parameters for SV_scripts.py by running the follwing commands, and the parameters are just self-explanatory.

      cd ./Tailored_SV_thala/
      vi SV_configure_file.txt

* Step4: generate the structured folder layers and PBS scripts by running the following commands:

      python SV_scripts.py

After Step4, you will have the follwing structure:

    | -- /home/data/Thala/SV
    |   | -- Tailored_SV_thala
    |   |   | ... ...
    |   |   | ... ...
    |   |   | all the supproting scripts(Don't run or change them, just leave them there)
    |   |   | ... ...
    |   |   | ... ...
    |   | -- Screening_stage
    |   |   | -- Conifer
    |   |   |    | -- RPKM_cal.pbs
    |   |   |    | -- Conifer_Run.pbs
    |   |   |    | -- RPKM
    |   |   | -- BreakDancer
    |   |   |    | -- BreakDancer_Run.pbs
    |   |   | -- Pindel
    |   |   |    | -- Pindel_Run.pbs
    |   | -- FineProfiling_stage
    |   |   | -- Conifer


* Step5: go to the Screening_stage folder, and run these scripts by qsub(PBS platform) or bash(PBS-free platform) for  BreakDancer, Pindel and Conifer.

BreakDancer should go before Pindel, since results from BreakDancer are used as one of the input for Pindel

After BreakDancer and Pindel, we run Conifer: first calculate RPKM, then run the Conifer main process.

      cd /home/data/Thala/SV/Screening_stage/BreakDancer
      qsub BreakDancer_Run.pbs
      cd /home/data/Thala/SV/Screening_stage/Pindel
      qsub Pindel_Run.pbs
      cd /home/data/Thala/SV/Screening_stage/Conifer
      qsub RPKM_cal.pbs
      qsub Conifer_Run.pbs

Here, for the screening purpose, we only focus on known causal SVs. Users could writing their own scripts to filter the resutls.

**Results for screening_stage** are stored in the following files:

    | -- /home/data/Thala/SV
    |   | -- Tailored_SV_thala
    |   |   | ... ...
    |   |   | ... ...
    |   |   | all the supproting scripts(Don't run or change them, just leave them there)
    |   |   | ... ...
    |   |   | ... ...
    |   | -- Screening_stage
    |   |   | -- BreakDancer
    |   |   |    | -- BD_pre/QCed_Report/BD_Causal.pre
    |   |   | -- Pindel
    |   |   |    | -- P_pre
    |   |   |    |   | - chr16/QCed_Report/Causal_Pindel_Deletion.pre
    |   |   |    |   | - chr11/QCed_Report/Causal_Pindel_Deletion.pre
    |   |   | -- Conifer
    |   |   |    | -- QCed_Report/Conifer_Deletion_Causal.pre
                                 /Alpha_region_Conifer_Duplication.pre

* Step6: Fine-profiling stage(if necessary)

Since read-depth method is a comparative method, it is sensitive to sample size. In practise, at least 8 samples from the same batch and carrying the same large deletions are exptected in fine-profiling stage.

For example, when you detected 20 --SEA deletion carriers, then you can let these 20 --SEA carriers to go through the fine-profiling stage to further determine their poteintial compound heterozygous status, such as --SEA/-a3.7 in Hb H disease. Otherwise, fine-profiling stage testing maybe biased, in which more samples are needed.

Here, we give an example showing the general process, users please take 5 minites to learn and then decide whether this applies to your situations.

**(i) merge BreakDancer and Pindel calling, and define sample list with deletions covering both the HBA2 and HBA1 regions**

    cd /home/data/Thala/SV/FileProfiling_stage/Conifer
    qsub Fine_profiling_list.pbs

**(ii) Manually check the carrier counts for each large deletions in the following files**

    Fine_Profiling_list.sorted_uniq_Raw_P_BD_merge.pre

Let's say, if you find 20(sample size >8 is OK) --SEA carriers, then you can continue.

    mkdir RPKM(/home/data/Thala/SV/FineProfiling_Stage/Conifer/RPKM)

Then,

**(iii) Copy these 20 --SEA carriers' RPKM files from the Screening_stage/Conifer/RPKM folder to the RPKM folder you just created**

**(iv) Run the Conifer scripts and check the resutls**

    cd /home/data/Thala/SV/FileProfiling_stage/Conifer
    qsub FP_step1_main_run_Conifer.pbs

**The results file are in:**

    /home/data/Thala/SV/FineProfiling_stage/Conifer/QCed_Report/Conifer_Deletion_Causal.pre
                                                                /Alpha_region_Conifer_Duplication.pre

## License

This project is licensed under GNU GPL v3.

## Authors

Cao Yujie(The University of Hong Kong)
