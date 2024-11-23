import pandas as pd
from Bio import SeqIO
import json

reader = lambda x: pd.read_csv(x, sep='\t').sort_values(['genome','score'],ascending=[True,False]).drop_duplicates('genome')
SeqDetails= lambda seq:{'seq':seq,'A':seq.count('A'),'A':seq.count('A'),'C':seq.count('C'),'T':seq.count('T'),'G':seq.count('G'),'N':seq.count('N'),'len':len(seq)}

def SeqFetcher(fileName:str):
    record={}
    df=pd.read_csv(fileName.replace('.fa','.tsv'),sep='\t')
    df['index']=df['index'].astype(int)
    for i in SeqIO.parse(fileName,'fasta'):
        try:
            key1=i.id.split('_')[0]
            key2=int(i.id.split('_')[1])
            seq=i.seq
            temp={key2:SeqDetails(seq=seq)}
            temp[key2].update({'score':df.at[(key1,key2),'score']})
            if key1 not in record.keys():
                record[key1]=temp
            else:
                record[key1].update(temp)
        except:
            print(key1,key2,fileName)
            raise Exception
    yield from record.items()

def writer(output:str,records:dict):
    with open(output,'a') as f:
        for _id,_seq in records.items():
            _=f.write(f'>{_id}\n{_seq['seq']}\n')

def NFilter(fastaFile:str,errorFile:str):
    fastaRecord=SeqFetcher(fastaFile)
    filterFastaRecord={}
    for organism,record in fastaRecord:
        resultRecord={}
        for _i,SeqInformation in record.items():
            if SeqInformation['N']!=0:
                continue
            else:
                resultRecord[_i]=SeqInformation
        if bool(resultRecord):
            _index=ScoreFilter(resultRecord)
            filterFastaRecord[organism]=resultRecord[_index]
        else:
            with open(errorFile,'a') as f:
                _=f.write(f'{organism}\n')
    return filterFastaRecord
                
def ScoreFilter(fastaRecord:dict):
    score_list=[]
    index_list=[]
    for _i,seqInformation in fastaRecord.items():
        index_list.append(_i)
        print(seqInformation)
        score_list.append(seqInformation['score'])
    return index_list[score_list.index(max(score_list))]
    
def main(fastaFolder:str):
    from os import listdir
    mainPath='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/rnaSeq'
    files=[f'{fastaFolder}/{i}' for i in listdir(fastaFolder) if '.fa' in i]
    for file in files:
        sType=file.split('.')[0].split('/')[-1]
        errorFile=f'{mainPath}/{sType}_error.txt'
        output=f'{mainPath}/{sType}.fasta'
        record=NFilter(fastaFile=file,errorFile=errorFile)
        writer(output=output,records=record)

def argumentParser(configFile:str):
    from json import load
    with open(configFile, 'r') as config_file:
        config = load(config_file)
    fastaFolder=config['fastaFolder']
    main(fastaFolder=fastaFolder)
        
    
if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/scripts/seqFetcherRNA.json'
    argumentParser(configFile)
    
                                
    
    
    
    

