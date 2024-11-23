import pandas as pd
from math import log2
from multiprocessing import Pool
from os import listdir,path

def filterDF(fileName:str,threshold_p=0.999):
    orgName=fileName.split('/')[-1].split('.',1)[0]
    threshold=log2(threshold_p/(1-threshold_p))
    df=pd.read_csv(fileName,sep='\t',index_col=0)
    df=df[(df['E-value']<=.001) & (df['score']>=threshold)]
    if df.empty:
        return df,{orgName:0}
    else:
        df['OrgName']=orgName
        df.set_index('OrgName',inplace=True)
        df=df.sort_values('score',ascending=False).drop_duplicates(['query_name'])
        return df,{orgName:df.shape[0]}

def worker(_input_:str,_output_:str,threshold_p=0.999):
    df,result_dict=filterDF(_input_,threshold_p=threshold_p)
    if df.empty:
        return result_dict
    else:
        df.to_csv(_output_,sep='\t')
        return result_dict

def multiWorker(inputFolder:str,outputFolder:str,finalMatrix:str,ncores:int):
    argument=[(path.join(inputFolder,i),path.join(outputFolder,i.split('.',1)[0]+'.filtered.tsv')) for i in listdir(inputFolder)]
    with Pool(ncores) as pool:
        result=pool.starmap(worker,argument)
    result = pd.DataFrame.from_dict({k: v for d in result for k, v in d.items()}, orient='index')
    result.index.name='Organism'
    result.columns=['ZnBR_Count']
    result.to_csv(finalMatrix,sep='\t')

def main(configFile:str):
    from json import load
    with open(configFile, 'r') as config_file:
        config = load(config_file)
    __input__ = config['inputFolder']
    __output__ = config['outputFolder']
    __finalMatrix__=config['finalMatrix']
    __ncores__=int(config['ncores'])
    multiWorker(inputFolder=__input__,outputFolder=__output__,finalMatrix=__finalMatrix__,ncores=__ncores__)

if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/hmmscan/scripts/ZnBRProteinList.config'
    main(configFile=configFile)

    