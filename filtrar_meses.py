from calendar import month_abbr
import locale
from typing import Union
import pandas as pd

def count_sum_group_by_month(df: pd.DataFrame, date_col: str, count_col: str, language: str='pt_BR', months: list = None) -> Union[pd.DataFrame, None]:
    try:      
        # set the locale
        locale.setlocale(locale.LC_TIME, f'{language}.utf8')
        
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
    
def count_sum_group_by_month_by_category(df: pd.DataFrame, date_col: str, count_col: str, category_col: str = 'Categoria', language: str='pt_BR', months: list = None) -> Union[pd.DataFrame, None]:
    try:
    # Set the locale
        locale.setlocale(locale.LC_TIME, f'{language}.utf8')
        
        # Filter dataframe by month if specified
        if months:
            mask = df[date_col].apply(lambda x: x.strftime("%b").upper() in months)
            df = df[mask]
            
        # Get a list of unique categories
        categories = df[category_col].unique()

        # Extract the month names from the dates columns, transform to abreviations with 3 uppercases uniques letters 
        month_names_index = df[date_col].apply(lambda x: month_abbr[x.month].upper()).unique()
        
        # Create a new DataFrame with the months as the index
        result = pd.DataFrame(index = month_names_index, 
                              columns = categories)
        
        # Fill the new DataFrame with the count of students for each month and category
        for category in categories:
            mask = df[category_col] == category
            
            take_the_mouth_of_the_date = df[date_col].apply(lambda x: month_abbr[x.month].upper())
            
            temp_df = df[mask].groupby(take_the_mouth_of_the_date)[count_col].sum()
            
            result[category] = temp_df
            
        return result.fillna(0).astype(int)
    
    except Exception as e:
        print(f'An error occurred: {e}')
        return None