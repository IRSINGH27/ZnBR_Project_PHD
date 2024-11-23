import pandas as pd
import json

reader = lambda x: pd.read_csv(x, sep='\t', index_col=0)

def process(_input_: str):
    df = reader(_input_)
    df = df.loc[df.draft_quality == 'high']
    return df

def argumentReader(config_path:str):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    input_path = config['_input_']
    output_path = config['_output_']
    return input_path,output_path

def main(_input_:str,_output_:str):
    df = process(_input_)
    df.to_csv(_output_,sep='\t')
    return None

if __name__ == '__main__':
    # Pass the path to the configuration file
    config_path = 'organismSelect.json'
    _input_,_output_=argumentReader(config_path=config_path)
    main(_input_,_output_)
