#!/bin/bash
#$ -S /bin/bash
#$ -wd /data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/scripts
#$ -q all.q@anomandaris.local
#$ -r y
#$ -j y
#$ -o ./logs/
#$ -pe mpi 100
#$ -N muscleRNASeq

source /home/aswin/irsingh/.bashrc
source /home/aswin/irsingh/softwares/miniconda3/bin/activate seqTools

seqFile="/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/16SrRNA_filtered.nondup.fna"
name="/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/msa/16SrRNA_filtered.nondup.@.afa"

echo "start"
muscle -super5 $seqFile -output $name -threads 100 -perm all;

echo "done all"