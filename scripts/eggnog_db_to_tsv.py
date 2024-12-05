
def main(db_file:str,table_name:str,output:str):
    import sqlite3
    import pandas as pd
    conn=sqlite3.connect(db_file)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    df.to_parquet(output)

if __name__=='__main__':
    from json import load
    configFile='/data/irsingh/Zinc_Work/WoL_reset_18Nov2025/scripts/eggnog_db_to_tsv.json'
    with open(configFile) as f:
        config=load(f)
    main(db_file=config['db_file'],table_name=config['table_name'],output=config['output'])
