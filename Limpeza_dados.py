import pandas as pd
from typing import Union

def limpar_dados(file_path:str , columns_to_drop : list  = None, column_to_strip: list = None)-> Union[pd.DataFrame,None]:
    if columns_to_drop:
        base_dados_csv = pd.read_csv(file_path).drop(columns=columns_to_drop)
    else:
        base_dados_csv = pd.read_csv(file_path)
    # Trim whitespace from Columns Names    
    base_dados_csv.columns = base_dados_csv.columns.str.strip()
    
    # Erase blank spaces
    if column_to_strip:
        base_dados_csv[column_to_strip] = base_dados_csv[column_to_strip].apply(lambda x: x.str.strip())
    else:
        trim_strings = lambda x: x.strip() if isinstance(x, str) else x
        base_dados_csv = base_dados_csv.applymap(trim_strings)
    
    pd_dados_com_date = converter_coluna_data_em_datatime(base_dados_csv,'Data')
    
    return pd_dados_com_date

def converter_coluna_data_em_datatime(df, date_column):
    
    # Convert the date_column to datetime objects
    df['Data'] = pd.to_datetime(df[date_column], format = r"%d/%m/%Y")

    # Format the date strings to dd/mm/yyyy
    df['Data'] = df['Data'].dt.date
    
    return df