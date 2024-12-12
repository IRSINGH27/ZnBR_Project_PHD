def fileReader(fileName:str,threshold:float):
    import pandas as pd
    from os.path import basename
    df=pd.read_csv(fileName,sep='\t',index_col=0)
    df.columns=['absence','presence']
    df.index=[int(i) for i in df.index]
    df.index.name='Node'
    df=pd.DataFrame(df.presence>=threshold)
    colName=basename(fileName).split('_asr')[0].replace('_','',1)
    df.columns=[colName]
    return df

def multiWorker(folderName:str,ncores:int,threshold:float):
    from os import path,listdir
    from multiprocessing import Pool
    arguments=[(path.join(folderName,i),threshold) for i in listdir(folderName) if 'likanc' in i]
    with Pool(ncores) as pool:
        result=pool.starmap(fileReader,arguments)
    return result

def main(configFile:str):
    import pandas as pd
    from json import load
    with open(configFile,'r') as f:
        config=load(f)
    
    records=multiWorker(folderName=config['folderName'],ncores=int(config.get('ncores',1)),threshold=float(config.get('threshold',.75)))
    df=pd.concat(records,axis=1)
    df.astype(int).to_csv(config['output'],sep='\t')
    return None


if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/Ancestral_State_Reconstruction/16S_rRNA/scripts/nodeASRMatrix.json'
    main(configFile=configFile)