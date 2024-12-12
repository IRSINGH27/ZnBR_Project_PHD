import pandas as pd
import re
from os import path,listdir

def process1(fileName:str):
    cogCat=re.findall(r'cogCat_[a-zA-Z]+',fileName)
    df=pd.read_csv(fileName,sep='\t',index_col=0)
    df=pd.DataFrame(df.sum(axis=1))
    if cogCat=='a':
        print(fileName)
    try:
        df.columns=cogCat
    except Exception as e:
        print(cogCat)
        print(fileName)
        raise e
    return df

def process2(inputFolder:str):
    files=listdir(inputFolder)
    totalFile=pd.DataFrame(pd.read_csv([path.join(inputFolder,i) for i in files if 'cogCat' not in i][0],sep='\t',index_col=0).sum(axis=1))
    totalFile.columns=['eggNOG_Total']
    cogCatFiles=[process1(path.join(inputFolder,i)) for i in files if 'cogCat' in i]
    cogCatDF=pd.concat(cogCatFiles,axis=1).fillna(0)
    finalDF=pd.concat([totalFile,cogCatDF],axis=1)
    return finalDF

def main(configFile:str):
    from json import load
    with open(configFile,'r') as f:
        config=load(f)
    df=process2(config['inputFolder'])
    df.to_csv(config['outputFile'],sep='\t')

if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/organismMatrix/scripts/hmmscan/eggJoiner.json'
    main(configFile)