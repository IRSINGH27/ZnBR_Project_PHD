import pandas as pd
from os import listdir,path

def proteomSize(fileName:str):
    from gzip import open as gopen
    from Bio.SeqIO import parse
    with gopen(fileName,'rt') as content:
        lenP=0
        for i in parse(content,'fasta'):
            lenP+=1
    return fileName.split('.',1)[0].split('/')[-1],lenP

def multiWorker(seqDir:str,ncores:int):
    from multiprocessing import Pool
    arguments=[path.join(seqDir,i) for i in listdir(seqDir)]
    with Pool(ncores) as pool:
        result=pool.map(proteomSize,arguments)
    return result

def matrixMaker(seqDir:str,znbrFile:str,phylumInfo:str,ncores:int):
    znbrDF=pd.read_csv(znbrFile,sep='\t',index_col=0)
    proteomDF=pd.DataFrame(multiWorker(seqDir=seqDir,ncores=ncores))
    phylumDF=pd.read_csv(phylumInfo,sep='\t',index_col=0)
    phylumDF.index=phylumDF.assembly_accession.apply(lambda x:x.split('.',1)[0])
    phylumDF.index.name='org'
    phylumDF=phylumDF.loc[:,['superkingdom','phylum','class','order','family','genus','species']]
    znbrDF.index.name='org'
    proteomDF.columns=['org','pLen']
    proteomDF.set_index('org',inplace=True)
    x=proteomDF.index
    return pd.concat([znbrDF.loc[x],proteomDF.loc[x],phylumDF.loc[x]],axis=1)

def main(configFile:str):
    from json import load
    with open(configFile, 'r') as config_file:
        config = load(config_file)
    seqDir = config['seqDir']
    znbrFile = config['znbrFile']
    phylumInfo = config['phylumInfo']
    ncores = int(config['ncores'])
    output = config['output']
    matrixMaker(seqDir=seqDir,znbrFile=znbrFile,phylumInfo=phylumInfo,ncores=ncores).to_csv(output,sep='\t')

if __name__=='__main__':
    config='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/organismMatrix/scripts/matrixMaker.config'
    main(configFile=config)

