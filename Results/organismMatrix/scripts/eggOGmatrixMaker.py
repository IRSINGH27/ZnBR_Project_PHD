import pandas as pd

def fileReader(fileName:str):
    df=pd.read_csv(fileName,header=None,comment='#',sep='\t')
    with open(fileName,'r') as content:
        colNames=[i.strip().split('\t') for i in content.readlines() if '#query' in i][0]
    df.columns=colNames
    return df

def matrixMaker(df:pd.DataFrame,outputFile:str):
    df=df.loc[:,['#query','eggNOG_OGs']]
    df['Org']=df['#query'].apply(lambda x:x.split('|')[0])
    df.eggNOG_OGs=df.eggNOG_OGs.str.split('@',expand=True)[0]

    matrixDF=pd.DataFrame(0,index=df.Org.unique(),columns=df.eggNOG_OGs.unique())
    for org in matrixDF.index:
        _=df.loc[df.Org==org,'eggNOG_OGs']
        if type(_)!=str:
            _=_.value_counts()
            matrixDF.loc[org,_.index.values]=_.values
        else:
            matrixDF.loc[org,_]=1
    matrixDF.to_csv(f"{outputFile}_absoulteCount.tsv",sep='\t')
    matrixDF.astype(bool).astype(int).to_csv(f"{outputFile}_binary.tsv",sep='\t')
    return None

def functionalDivider(df:pd.DataFrame,outputFile:str):
    from re import findall
    annotatedDF=df.loc[df.COG_category!='-']
    annotatedDF.COG_category=annotatedDF.COG_category.apply(lambda x:findall(r'\w',x))
    annotatedDF=annotatedDF.explode('COG_category')
    nonAnnotatedDF=df.loc[df.COG_category=='-']
    matrixMaker(nonAnnotatedDF,f'{outputFile}_cogCat_nonannotated')
    for cat in annotatedDF.COG_category.unique():
        tempDF=annotatedDF.loc[annotatedDF.COG_category==cat]
        neoOutputFile=f'{outputFile}_cogCat_{cat}'
        matrixMaker(tempDF,neoOutputFile)
    
def main(configFile:str):
    from json import load
    with open(configFile,'r') as f:
        config=load(f)
    df=fileReader(config['fileName'])
    matrixMaker(df,outputFile=config['outputFile'])
    functionalDivider(df,outputFile=config['outputFile'])
    return None


if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/organismMatrix/scripts/eggOGmatrixMaker.json'
    main(configFile=configFile)
    