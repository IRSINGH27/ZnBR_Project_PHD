import pandas as pd
from os import listdir,path
import multiprocessing as mp

def hmmResultLoader(file:str,db_name:str):
    df=pd.read_csv(file,sep='\t',index_col=0)
    df=df.reset_index().set_index('target_name')
    db=pd.read_parquet(db_name)
    commonCOG=list(set(df.index).intersection(db.index))
    df.loc[commonCOG,'description']=db.loc[commonCOG,'description']
    df.loc[commonCOG,'COG_categories']=db.loc[commonCOG,'COG_categories']
    return df.reset_index().set_index('OrgName')

def multiWorker(inputFolder:str,db_name:str,ncores=1):
    arguments=[]
    for file in listdir(inputFolder):
        _=(path.join(inputFolder,file),db_name)
        arguments.append(_)
    with mp.Pool(ncores) as pool:
        result=pool.starmap(hmmResultLoader,arguments)
    finalDF=pd.concat(result)
    finalDF.index=finalDF.index.astype('category')
    finalDF['description']=finalDF['description'].fillna('-')
    for col in finalDF.columns:
        finalDF[col]=finalDF[col].astype('category')
    return finalDF

def main(configFile:str):
    from json import load
    with open(configFile) as f:
        config=load(f)
    annoatedDF=multiWorker(inputFolder=config['inputFolder'],db_name=config['db_name'],ncores=int(config['ncores']))
    annoatedDF.to_parquet(config['output'])
    return None


if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/hmmscan/scripts/eggCOGCatAdding.json'
    main(configFile=configFile)