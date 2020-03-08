# tailored_SV_thala

This repository describes the general workflow for thalassaemia structural variation(SV) detection. Common thalassaemia SV includes deletions and du(tri)plications, such as South East Type deletion(--SEA), alpha-3.7kb deletion(-a3.7) and alpha-4.2kb deletion(-a4.2), depending on the local epidemiology.

Here, we want to emphasize that the input alignment BAM files should **not** go through rescue process in point mutation/Indel detection paradigm. If you start with a large BAM file from whole genome sequencing, you are suggested to extract BAM records within the hemoglobin regions to accelerate the calling process, and perhapes the command likes:

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

Besides, a two-stage strategy is used to get a confident SV prediction:

In the first **screening stage**, all the samples will be pooled and tested together. Then, samples with large deletions(>10k) will be labeled as Group I, while others are labeled as Group II.

In the next **fine profiling stage**, depth change profiles will be updated within each group before the interpretation of the mutation.

bedtools should be in your environments

## Step-by-step description for thalassaemia SV detection

This working example help users to generate structured folder layers and PBS scripts for job submission. However, these PBS files can also be run by bash(sh) on servers that are PBS-free.

* Step1: install the forementioned software, [BreakDancer](https://github.com/genome/breakdancer), [Pindel](https://github.com/genome/pindel) and [Conifer](http://conifer.sourceforge.net/).

* Step2: download this repository to the working directory(such as /home/data/Thala/SV/)by running the follwing commands:

      cd /home/data/Thala/SV/
      git clone https://github.com/JavenCao/Tailored_SV_thala.git

You will need the [Anaconda](https://docs.conda.io/en/latest/) for Python package manager for Conifer:

    cd ./Tailored_SV_thala/tailored_SV_Thala/
    conda env create --file environment.yml

* Step3: set parameters for SV_scripts.py by running the follwing commands:

      cd ./Tailored_SV_thala/tailored_SV_Thala/
      vi SV_configure_file.txt

* Step4: generate the structured folder layers and PBS scripts by running the following commands:

      python SV_scripts.py

After Step4, you will have the follwing structure:

    | -- /home/data/Thala/SV
    |   | -- Tailored_SV_thala
    |   |   | -- all the supproting scripts(Don't run or change them, just leave them there)
    |   |   | ... ...
    |   |   | -- Screening_stage
    |   |   |   | -- Conifer
    |   |   |   |    | -- RPKM_cal.pbs
    |   |   |   |    | -- Conifer_Run.pbs
    |   |   |   |    | -- RPKM
    |   |   |   | -- BreakDancer
    |   |   |   |    | -- BreakDancer_Run.pbs
    |   |   |   | -- Pindel
    |   |   |   |    | -- Pindel_Run.pbs

* Step5: go to the Screening_stage folder, and run these scripts by qsub(PBS platform) or bash(PBS-free platform) for Conifer, BreakDancer, Pindel.

Conifer: first calculate RPKM, then call the CNVs.

      cd ./Tailored_SV_thala/tailored_SV_Thala/Conifer
      qsub Conifer_Run.pbs

BreakDancer should go before Pindel, since results from BreakDancer are used as one of the input for Pindel

    | -- /home/data/Thala/SV
    |   | -- Tailored_SV_thala
    |   |   | -- all the supproting scripts(Don't run or change them, just leave them there)
    |   |   | ... ...
    |   |   | -- Screening_stage
    |   |   |   | -- Conifer
    |   |   |   |    | -- RPKM_cal.pbs
    |   |   |   |    | -- Conifer_Run.pbs
    |   |   |   |    | -- RPKM
    |   |   |   | -- BreakDancer
    |   |   |   |    | -- BreakDancer_Run.pbs
    |   |   |   | -- Pindel
    |   |   |   |    | -- P_pre
    |   |   |   |    |    | -- chr16/QCed_Report/Causal_Pindel_Deletion.pre
    |   |   |   |    |    | -- chr11/QCed_Report/Causal_Pindel_Deletion.pre

Here, for the screening purpose, we only focus on known causal SVs. Users could writing their own scripts to filter the resutls.

Raw results are stored in the following folders for the Pindel, BreakDancer and Conifer:

    | -- /home/data/Thala/SV
    |   | -- Tailored_SV_thala
    |   |   | -- all the supproting scripts(Don't run or change them, just leave them there)
    |   |   | ... ...
    |   |   | -- Screening_stage
    |   |   |   | -- Conifer
    |   |   |   |    | -- CNVcalls.txt
    |   |   |   | -- BreakDancer
    |   |   |   |    | -- BD_pre/(All files)
    |   |   |   | -- Pindel
    |   |   |   |    | -- P_Pre/(All files)


## License

This project is licensed under GNU GPL v3.

## Authors

Cao Yujie(The University of Hong Kong)
