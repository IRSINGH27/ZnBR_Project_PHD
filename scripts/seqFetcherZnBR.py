import multiprocessing as mp
import numpy as np

def pandasFileReader(fileName:str,threshold_p=.999):
    import re
    import pandas as pd
    from math import log2
    orgName=re.findall(r'GC[AF]_\d+',fileName)[0]
    df=pd.read_csv(fileName,sep='\t',index_col=0)
    threshold=log2(threshold_p/(1-threshold_p))
    df=df[(df['E-value']<=.001) & (df['score']>=threshold)]
    df=df.sort_values('score',ascending=False).drop_duplicates(['query_name'])
    return orgName,df.query_name.unique()

def seqFetcher(seqFilePath: str, outputPath: str, proteinList: np.array,orgName:str):
    import gzip
    from os import listdir
    from Bio import SeqIO
    filepath=[i for i in listdir(seqFilePath) if orgName in i][0]
    with gzip.open(f'{seqFilePath}/{filepath}','rt') as fasta:
        with open(f'{outputPath}/{orgName}_znbr.faa','w') as f:
            for i in SeqIO.parse(fasta,'fasta'):
                if not i.id in proteinList:
                    continue
                else:
                    f.write(f'>{i.id}\n{i.seq}\n')
    return None

def main(inputName:str,seqFilePath:str,outputFolder:str,ncores:int):
    from os import listdir
    arguments=[]
    for pandasFile in listdir(inputName):
        orgName,proteinList=pandasFileReader(f'{inputName}/{pandasFile}')
        arguments.append((seqFilePath,outputFolder,proteinList,orgName))
    with mp.Pool(ncores) as pool:
        pool.starmap(seqFetcher,arguments)
    return None

def worker(configFile:str):
    from json import load
    with open(configFile, 'r') as config_file:
        config = load(config_file)
    inputFile=config['inputFile']
    outputFolder=config['outputFolder']
    ncores=int(config['ncores'])
    seqFilePath=config['seqFilePath']
    main(inputName=inputFile,outputFolder=outputFolder,ncores=ncores,seqFilePath=seqFilePath)
    return None

if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/scripts/seqFetcherZnBR.json'
    worker(configFile=configFile)
