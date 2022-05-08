import pandas as pd
import json

def reformatEU(target_df: pd.DataFrame, 
               eurozone_countries: str) -> pd.DataFrame:
    '''
    Expand abbreviation for EU to specify all Eurozone countries
    
    Args:
        target_df (pandas.DataFrame): the dataframe that will receive updates
        eurozone_countries (str): path to eurozone index
    Returns:
        pandas.DataFrame: expanded version of the initial target_df
    '''
    eurozone_index = pd.read_csv(eurozone_countries, parse_dates=["Adoption"])
    eurozone_index = eurozone_index[eurozone_index.Adoption <= target_df.loc[0].date]
    for country in tuple(eurozone_index.ISO2):
        target_df[country] = target_df["XM"]
    
    return target_df

def reassignISO2toISO3(target_df: pd.DataFrame, 
                       iso_conversions: str) -> pd.DataFrame:
    '''
    Replace ISO2 with ISO3 values
    
    Args:
        target_df (pandas.DataFrame): the dataframe that will receive updates
        iso_conversions (str): path to file with iso2 to iso3 conversions
    Returns:
        pandas.DataFrame: updated target_df
    '''
    
    with open(iso_conversions) as json_file:
        ISO_conversions = json.load(json_file)
    
    return target_df.replace(ISO_conversions)
    
    
def getInterestRates(cutoff_date: str, 
                     ir_path: str, 
                     iso_conversions: str, 
                     iso_to_country_name: str) -> pd.DataFrame:
    '''
    Convert data from BIS into a vertical dataframe
    
    Args:
        cutoff_date (str): the last date for which data is to be extracted
        ir_path (str): path to the file with interest rates
        iso_conversions (str): path to the file with ISO-2 to ISO-3 conversions
        iso_to_country_name (str): path to the file with ISO-3 to name conversions
        eu_countries (str): path to the file with 
    Returns:
        pandas.DataFrame: dataframe with columns "date", "ISO3", "name", "interest rate"
    
    '''
    df = pd.read_csv(ir_path)
    
    target_df = df[df.columns[list(df.columns).index(cutoff_date):]].T
    target_df.columns = list(df["REF_AREA"])
    target_df = target_df.reset_index().rename(columns={"index":"date"})
    target_df.date = pd.to_datetime(target_df.date)
    target_df = target_df.ffill()
    
    
    return target_df
    
def formatIRData(cutoff_date: str, 
                 ir_path: str, 
                 iso_conversions: str, 
                 iso_to_country_name: str, 
                 eurozone_countries: str) -> pd.DataFrame:
    '''
    Convert data from BIS into a vertical dataframe with detailed EU countries
    
    Args:
        cutoff_date (str): the last date for which data is to be extracted
        ir_path (str): path to the file with interest rates
        iso_conversions (str): path to the file with ISO-2 to ISO-3 conversions
        iso_to_country_name (str): path to the file with ISO-3 to name conversions
        eurozone_countries (str): path to the file with 
    Returns:
        pandas.DataFrame: dataframe with columns "date", "ISO3", "name", "interest rate", "text
    '''
    
    target_df = getInterestRates(cutoff_date, ir_path, iso_conversions, iso_to_country_name)
    
    target_df = reformatEU(target_df, eurozone_countries)
    
    target_df = pd.melt(target_df, id_vars=["date"], var_name="ISO3", value_name="interest rate")
    target_df = reassignISO2toISO3(target_df, iso_conversions)
    target_df = target_df.merge(pd.read_csv(iso_to_country_name, encoding='latin1'))
    target_df["text"] = target_df.apply(lambda row: f"{row['name']}<br>{row['interest rate']}%", axis=1)

    return target_df[["date", "ISO3", "name", "interest rate", "text"]]