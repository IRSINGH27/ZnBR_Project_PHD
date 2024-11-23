import multiprocessing as mp

def ftpLinkGenerator(fileName:str):
    import pandas as pd
    df=pd.read_csv(fileName,sep='\t',index_col=0)
    df.ftp_path=df.ftp_path.apply(lambda x:x.replace('ftp://','https://'))
    return tuple([df.loc[i,'ftp_path'] for i in df.index])

def downloadLinkGenerator(ftpLink: str, output: str,protein:bool):
    import requests
    import os
    name = ftpLink.split('/')[-1]
    if protein:
        file_name = f'{name}_protein.faa.gz'
    else:
        file_name = f'{name}_genomic.fna.gz'  
    full_url = f'{ftpLink}/{file_name}'
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        output_path = os.path.join(output, file_name)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.RequestException as e:
        print(f'{name}\t{e}')
    except Exception as e:
        print(f'{name}\t{e}')
    return None

def main(inputName:str,outputFolder:str,ncores:int,protein:bool):
    linksTuple=ftpLinkGenerator(fileName=inputName)
    argument=tuple([(i,outputFolder,protein) for i  in linksTuple])
    with mp.Pool(ncores) as pool:
        pool.starmap(downloadLinkGenerator,argument)
    return None

def worker(configFile:str):
    from json import load
    with open(configFile, 'r') as config_file:
        config = load(config_file)
    inputFile=config['inputFile']
    outputFolder=config['outputFolder']
    ncores=int(config['ncores'])
    protein=bool(config['protein'])
    main(inputName=inputFile,outputFolder=outputFolder,ncores=ncores,protein=protein)
    return None

if __name__=='__main__':
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/scripts/seqFetcherNCBI.json'
    worker(configFile=configFile)