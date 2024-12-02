#!/bin/bash

src_dir="/home/aswin/irsingh/softwares/miniconda3/envs/eggnogEnv/lib/python3.12/site-packages/data/hmmer/Bacteria/"
dest_dir="/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/eggnogHMMProfiles/"

# Create the destination directory if it doesn't exist
mkdir -p "$dest_dir"

# Process each file in the source directory
for i in "$src_dir"*.fa
do
	cp "$i" "$dest_dir$(basename "$i")"
done

