import pandas as pd
def converter_coluna_data_em_datatime(df, date_column):
    
    # Convert the date_column to datetime objects
    df['Data'] = pd.to_datetime(df[date_column], format = r"%d/%m/%Y")

    # Format the date strings to dd/mm/yyyy
    df['Data'] = df['Data'].dt.date
    
    return df