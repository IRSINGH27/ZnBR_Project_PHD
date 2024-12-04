def fastaWriter(writer,fastaFile:str):
    from re import findall
    from Bio import SeqIO
    orgName=findall(r'GC[AF]_\d+',fastaFile)[0]
    for record in SeqIO.parse(fastaFile,'fasta'):
        content=f'>{orgName}|{record.id}\n{record.seq}\n'
        _=writer.write(content)

def worker(_inputDir:str,_outputFile:str):
    from os import listdir,path
    files=listdir(_inputDir)
    concatFile=open(_outputFile,'w')
    for fastaFile in files:
        filePath=path.join(_inputDir,fastaFile)
        fastaWriter(concatFile,filePath)
    concatFile.close()

def main(configFile:str):
    from json import load
    with open(configFile, 'r') as config_file:
        config = load(config_file)
    inputDir=config['inputDir']
    outFile=config['outputFile']
    worker(_inputDir=inputDir,_outputFile=outFile)
    return None

if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/scripts/ZnBRProteinConcat.json'
    main(configFile=configFile)