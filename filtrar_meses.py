from calendar import month_abbr
import locale
from typing import Union
import pandas as pd

def count_sum_group_by_month(df: pd.DataFrame, date_col: str, count_col: str, language: str='pt_BR', months: list = None) -> Union[pd.DataFrame, None]:
    try:      
        # set the locale
        locale.setlocale(locale.LC_TIME, f'{language}.utf8')
        
        if "Todos" in months:
            return  df.groupby(df[date_col].apply(lambda x: x.month))[count_col].sum()
        
        # Filter the dataframe by month if the user specified month(s)
        if months:
            
            mask = df[date_col].apply(lambda x: x.strftime(r"%b").upper() in months)
            df = df[mask]
            
        # Group the data by month
        monthly_group = df.groupby(df[date_col].apply(lambda x: x.month))[count_col].sum()
        
        # Change the index names
        monthly_group.index = [month_abbr[i].upper() for i in monthly_group.index]
        monthly_group = monthly_group.rename_axis("Meses")
       
        return monthly_group
    except Exception as e:
        print(f'An error occurred: {e}')
        return None