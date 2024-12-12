
def filterDF(fileName:str,threshold_p=0.999):
    import re
    from numpy import log2
    import pandas as pd
    orgName=re.findall(r'GC[AF]_\d+',fileName)[0]
    threshold=log2(threshold_p/(1-threshold_p))
    df=pd.read_csv(fileName,sep='\t',index_col=0)
    df=df[(df['E-value']<=.001) & (df['score']>=threshold)]
    if df.empty:
        return None
    else:
        df['OrgName']=orgName
        df.set_index('OrgName',inplace=True)
        df=df.sort_values('score',ascending=False).drop_duplicates(['query_name'])
        df=df[['query_name','target_name']]
        return df

def multiWorker(inputFolder:str,finalMatrix:str,ncores:int):
    import pandas as pd
    from os import listdir,path
    from multiprocessing import Pool
    argument=[(path.join(inputFolder,i),.999) for i in listdir(inputFolder)]
    with Pool(ncores) as pool:
        result=pool.starmap(filterDF,argument)
    result=pd.concat(result)
    result.to_csv(finalMatrix,sep='\t')
    return None

def main(configFile:str):
    from json import load
    with open(configFile) as f:
        config=load(f)
    multiWorker(inputFolder=config['inputFolder'],finalMatrix=config['finalMatrix'],ncores=int(config.get('ncores',1)))
    return None

if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/hmmscan/scripts/ZnBRProtein2Model.json'
    main(configFile=configFile)