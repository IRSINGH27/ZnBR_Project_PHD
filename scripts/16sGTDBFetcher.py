import pandas as pd
from Bio import SeqIO
from re import findall
from json import load

def indexMaker(fileName:str):
    df=pd.read_csv(fileName,sep='\t',index_col=0)
    return {df.loc[i,'assembly_accession'].split('.')[0]:df.loc[i,'gtdb_id'].split('.')[0] for i in df.index}

def SeqFetcher(fileName:str,seqFile:str):
    orgDict=indexMaker(fileName=fileName)
    for i in SeqIO.parse(seqFile,'fasta'):
        try:
            _id_=findall(r'GC[AF]_\d+',i.id)
            if _id_:
                if _id_[0] in orgDict.keys():
                    yield _id_[0],str(i.seq)
        except:
            print(i.id)
            raise Exception

def writer(fileName:str,seqFile:str,output:str):
    with open(output,'w') as f:
        for head,sequence in SeqFetcher(fileName=fileName,seqFile=seqFile):
            _=f.write(f'>{head}\n{sequence}\n')
    return None

def main(configFile:str):
    with open(configFile, 'r') as config_file:
        config = load(config_file)
    fileName = config['fileName']
    seqFile = config['seqFile']
    output = config['output']
    writer(fileName=fileName,seqFile=seqFile,output=output)
    return None

if __name__=='__main__':
    config='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/scripts/16sGTDBFetcher.config'
    main(configFile=config)

