#!/bin/bash
#$ -S /bin/bash
#$ -wd /data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/scripts
#$ -q all.q@anomandaris.local
#$ -r y
#$ -j y
#$ -o ./logs/
#$ -pe mpi 5
#$ -N iqtree

source /home/aswin/irsingh/.bashrc
source /home/aswin/irsingh/softwares/miniconda3/bin/activate phyloEnv

msaFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/16SrRNA_filtered.nondup.trimal.afa'
prefix='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/tree/16SrRNA_tree'

echo "start"

iqtree -s $msaFile --prefix $prefix --safe --runs 3 -T AUTO --threads-max 5 -B 5000 --mset GTR --msub nuclear

echo "done all"