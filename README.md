# tailored_SV_thala

This repository describes the workflow for thalassaemia structural variants detection.

Here, we want to emphasize that the input alignment BAM file should **not** go through rescue process in point mutation/Indel detection paradigm.

For structural variation(SV) detection, the selected software, [BreakDancer](https://github.com/genome/breakdancer), [Pindel](https://github.com/genome/pindel) and [Conifer](http://conifer.sourceforge.net/) were jointly used with tailored parameters. More details about the parameter setting and processes can be found in the original publication.

Also, a two-stage strategy was used to get a confident SV prediction:

In the first **screening stage**, all the samples were pooled and tested together. Then, samples with large deletions(>10k) were labeled as Group I, while others were labeled as Group II.

In the next **fine profiling stage**, depth change profiles were updated within each group before the interpretation of the mutation.

## Step-by-step description for thalassaemia SV detection

* Step1: install the forementioned software.

* Step2: download this repository to the working directory(such as /home/data/Thala/SV/)by running the follwing commands:

      cd /home/data/Thala/SV/
      git clone URL

* Step3: set the parameter for SV_scripts.py by running the follwing commands:

      cd 
      vi SV_configure_file.txt
      
Most of the parameters are clear enough.

* Step4: generating the scripts for each program by running the following commands:

      python SV_scripts.py

* Step5: qsub scripts for Conifer, Pindel, BreakDancer



