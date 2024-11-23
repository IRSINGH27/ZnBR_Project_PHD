#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -q all.q@anomandaris.local
#$ -r y
#$ -j y
#$ -o ./logs/
#$ -pe mpi 50
#$ -N muscleRNASeq

source /home/aswin/irsingh/.bashrc
source /home/aswin/irsingh/softwares/miniconda3/bin/activate seqTools
seqFile='16SrRNA_afterFilter.nondup.fna'
name='./msa/16SrRNA_afterFilter.nondup'

echo "start"
muscle -super5 $seqFile -output $name.abc.$i.msa -threads 50 -perm abc;
muscle -super5 $seqFile -output $name.bca.$i.msa -threads 50 -perm bca;
muscle -super5 $seqFile -output $name.acb.$i.msa -threads 50 -perm acb;
muscle -super5 $seqFile -output $name.none.$i.msa -threads 50 -perm none;
wait
done

echo "done all"