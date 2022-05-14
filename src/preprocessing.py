import pandas as pd
import json
import streamlit as st 
from typing import Tuple, List, Union
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

@st.cache(suppress_st_warning=True)   
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


@st.cache(suppress_st_warning=True)
def getMonthly(df: pd.DataFrame, indicator: str, 
               iso_conversions: str, 
               date_range: tuple[str, str]=('1999-01', '2022-03'),
               interpolate: bool=True) -> pd.DataFrame:
    '''
    Reformat data for monthly visualisations
    
    Args: 
        df (pd.DataFrame): original dataframe
        iso_conversions (str): conversions for ISO2 to ISO3 conversions
        date_range (tuple[str, str]):
        interpolate (bool): choose whether to linearly interpolate data for 
        countries that have not posted it yet, set to False by default
    Returns:
        pd.DataFrame: formatted long dataframe
    '''
    df["Reference area"] = df["Reference area"].str[:2]
    countries = list(df["Reference area"])
    df = df[df.columns[list(df.columns).index(date_range[0]): list(df.columns).index(date_range[1])+1]].T
    df.columns = countries
    df = df.reset_index()
    df = df.rename(columns={"index":"date"})
    
    df = df.rename(columns = iso_conversions)
    
    if interpolate:
        return df.interpolate(method='linear', axis=1)
    else:
        return df

def splitDate(df: pd.DataFrame):
    '''
    Split data into month and year, converting them to int
    
    Args:
        df (pd.DataFrame): the dataframe that gets changed
    Returns:
        pd.DataFrame the edited dataframe
    '''
    df[["year", "month"]] = df['date'].str.split('-', 1, expand=True)
    df["year"] = df["year"].astype("int")
    df["month"] = df["month"].astype("int")
    
    return df[["year", "month", *df.columns[1:-2]]]

def expandCPIInterestRates(cpi_df: pd.DataFrame, ir_df: pd.DataFrame, eu_join: dict) -> pd.DataFrame:
    '''
    Combines CPI and Interest Rates data by BIS.org, expanding Eurozone interest rate to all Eurozone countries
    
    Args:
        cpi_df (pd.DataFrame): dataframe containing monthly CPI data by BIS.org
        cpi_df (pd.DataFrame): dataframe containing monthly CPI data by BIS.org
        eu_join (dict): a dictionary of Eurozone countries with years of entering
    Returns:
        combined and expanded pd.DataFrame  
    '''
    cpi_df = splitDate(cpi_df)
    ir_df = splitDate(ir_df)
    df = cpi_df.merge(ir_df, how="left")
    
    dfs = []
    for i in eu_join:
        dfs.append(pd.DataFrame({
                    "year" : df[(df.ISO3 == i) & (df.year >= eu_join[i])].year.values, 
                    "month": df[(df.ISO3 == i) & (df.year >= eu_join[i])].month.values, 
                    "ISO3" : df[(df.ISO3 == i) & (df.year >= eu_join[i])].ISO3.values,
                    "CPI"  : df[(df.ISO3 == i) & (df.year >= eu_join[i])].CPI.values,
                    "InterestRate": df[(df.ISO3 == "XM") & (df.year >= eu_join[i])].InterestRate.values}))
    df = ir_df.merge(cpi_df, how="left")
    
    return pd.concat([df, *dfs])

def getCombinedCPIInterestRates(cpi_path: str, ir_path: str,
                                iso_conversions_path: str,
                                eurozone_path: str,
                                interpolate:bool = True) -> pd.DataFrame:
    '''
    Prepare data from BIS.org for further analysis and visualisation
    
    Args:
        cpi_path (str):path to monthly CPI from BIS.org
        ir_path (str): path to monthly interest rates from BIS.org
        cutoff_date (str): cutoff date for data set as default to "1999-01-01"
        iso_conversions_path (str): path to the file containing ISO conversions
        eurozone_path (str): path to the file containing Eurozone countries and euro adoption dates
    
    Returns:
        pd.DataFrame:
    '''
    cpi_df = pd.read_csv(cpi_path)
    ir_df = pd.read_csv(ir_path)
    cpi_df = cpi_df[((cpi_df["Unit of measure"]=="771:Year-on-year changes, in per cent") 
              & (cpi_df["Frequency"] == "M:Monthly"))].reset_index(drop=True)
    
    iso_conversions = pd.read_csv(iso_conversions_path)
    iso_conversions_dict = dict(zip(iso_conversions.ISO2, iso_conversions.ISO3))
    
    cpi_df = getMonthly(cpi_df, "CPI", iso_conversions=iso_conversions_dict)
    ir_df = getMonthly(ir_df, "interest rate", iso_conversions=iso_conversions_dict)
    
    ir_df = ir_df.melt(id_vars="date", value_vars=ir_df.columns[1:], var_name="ISO3", value_name="InterestRate")
    cpi_df = cpi_df.melt(id_vars="date", value_vars=cpi_df.columns[1:], var_name="ISO3", value_name="CPI")
    
    eu_index = pd.read_csv(eurozone_path, parse_dates = ["Adoption"])
    eu_join=dict(zip(eu_index.ISO3, eu_index.Adoption.dt.year))
    df = expandCPIInterestRates(cpi_df, ir_df, eu_join)
    
    return df.merge(iso_conversions[["ISO3", "name"]])

def defineText(df: pd.DataFrame, indicators: Union[str, 
                                             Tuple[str, ...], 
                                             List[str]]) -> pd.DataFrame:
    '''
    Define text for hovertooltip in graphs
    
    Args:
        df (pd.DataFrame): dataframe with indicators that need to be formatted into text
        indicators (str, Tuple[str, ...], or List[str]): a list of indicators that need to be formatted
    Returns:
        pd.DataFrame the original dataframe with new columns
    '''
    if isinstance(indicators, str): 
        if indicators in df.columns:
            df[f"text_{indicators}"] = df.apply(lambda row: f"{row['name']}<br>{row[indicator]}%", axis=1)
        else:
            print(f"Indicator {indicators} not found")
            return df
    else:
        for indicator in indicators:
            df[f"text_{indicator}"] = df.apply(lambda row: f"{row['name']}<br>{row[indicator]: .2f}%", axis=1)
    return df