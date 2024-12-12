def seqDetails(record):
    a,g,t,c,n=record.seq.count('A'),record.seq.count('G'),record.seq.count('T'),record.seq.count('C'),record.seq.count('N')
    result={'id':record.id,'seq':record.seq,'Len':len(record.seq),'A':a,'G':g,'T':t,'C':c,'N':n}
    return result

def dataframeMaker(seqFile:str,output:str,ncores:int):
    import pandas as pd

    dataframe_record=multiWorker(seqFile=seqFile,ncores=ncores)
    df=pd.DataFrame(dataframe_record)
    df.to_csv(output,sep='\t')
    return df

def seqFilter(df,seqOutput:str):
    df=df[df.N==0]
    df.sort_values('Len',ascending=False,inplace=True)
    df.drop_duplicates('id',inplace=True,ignore_index=True)
    with open(seqOutput,'w') as seqFile:
        for header,seq in df.loc[:,['id','seq']].values:
            seqFile.write(f'>{header}\n{seq}\n')
    return None
    
def multiWorker(seqFile:str,ncores:int):
    from Bio import SeqIO
    from multiprocessing import Pool

    arguments=[record for record in SeqIO.parse(seqFile,'fasta')]
    with Pool(ncores) as pool:
        result=pool.map(seqDetails,arguments)
    return result

def main(configFile:str):
    from json import load
    
    with open(configFile,'r') as f:
        config=load(f)
    
    df=dataframeMaker(seqFile=config['seqFile'],output=config['dbOutput'],ncores=int(config.get('ncores',1)))
    seqFilter(df,config['seqOutput'])
    return None

if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/Results/treeMaking/16s_GTDB/scripts/seqFilter.json'
    main(configFile=configFile)
