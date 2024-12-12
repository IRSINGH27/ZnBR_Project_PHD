import pandas as pd

def fileReader(fileName:str):
    df=pd.read_parquet(fileName).reset_index()
    return df

def matrixMaker(df:pd.DataFrame,outputFile:str):
    matrixDF=df.pivot_table(index='OrgName', columns='target_name', aggfunc='size', fill_value=0,observed=False)
    matrixDF.to_csv(f"{outputFile}_absoulteCount.tsv",sep='\t')
    matrixDF.astype(bool).astype(int).to_csv(f"{outputFile}_binary.tsv",sep='\t')
    return None

def functionalDivider(df:pd.DataFrame,outputFile:str):
    from re import findall
    annotatedDF=df.loc[df.COG_categories!='-']
    annotatedDF.COG_categories=annotatedDF.COG_categories.astype(str).apply(lambda x:findall(r'\w',x))
    annotatedDF=annotatedDF.explode('COG_categories')
    nonAnnotatedDF=df.loc[df.COG_categories=='-']
    if not nonAnnotatedDF.empty:
        matrixMaker(nonAnnotatedDF,f'{outputFile}_cogCat_nonannotated')
    for cat in annotatedDF.COG_categories.unique():
        tempDF=annotatedDF.loc[annotatedDF.COG_categories==cat]
        neoOutputFile=f'{outputFile}_cogCat_{cat}'
        matrixMaker(tempDF,neoOutputFile)
        print(f'{cat} done')
    
def main(configFile:str):
    from json import load
    with open(configFile,'r') as f:
        config=load(f)
    df=fileReader(config['fileName'])
    matrixMaker(df,outputFile=config['outputFile'])
    functionalDivider(df,outputFile=config['outputFile'])
    return None


if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/organismMatrix/scripts/hmmscan/eggOGmatrixMaker.json'
    main(configFile=configFile)
    