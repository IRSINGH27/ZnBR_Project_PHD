#!/bin/bash

for i in "/home/aswin/irsingh/softwares/miniconda3/envs/eggnogEnv/lib/python3.12/site-packages/data/hmmer/Archaea/*.fa"
do
	cp $i "/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/eggnogHMMProfiles/$(basename $i)"
done

