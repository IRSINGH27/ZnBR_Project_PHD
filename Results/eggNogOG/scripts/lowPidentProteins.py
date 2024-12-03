def filterDF(configFile:str):
    import pandas as pd
    from json import load
    with open(configFile)  as content:
        config=load(content)
    df=pd.read_csv(config['fileName'],header=None,comment='#',sep='\t')
    with open(config['fileName'],'r') as content:
        colNames=[i.strip().split('\t') for i in content.readlines() if '#qseqid' in i][0]
    df.columns=colNames
    df=df[df.pident<float(config['threshold'])].reset_index(drop=True)
    df.to_csv(config['outputFile'],sep='\t')

if __name__=='__main__':
    filterDF("./lowPidentProteins.config")
