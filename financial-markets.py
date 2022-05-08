import streamlit as st
import pandas as pd
import numpy as np

st.title('Financial Markets')

import time
import datetime as dt

from datetime import datetime, date, time
from src.preprocessing import formatIRData
from src.charts import makeChoropleth
import plotly.graph_objects as go


cutoff_date = "1999-01-01"
ir_path = r"./data/WS_CBPOL_D_csv_col.csv"
iso_conversions = r"./data/iso_conversions.json"
iso_to_name_conversions = r"./data/iso_to_name.csv"
eurozone_countries = r"./data/eurozone.csv"

df = formatIRData(cutoff_date, ir_path, iso_conversions, iso_to_name_conversions, eurozone_countries)


st.header("Official Date Picker")
cols1,cols2 = st.columns((1,2)) # To make it narrower

current_date = cols1.date_input(
        'date', value=dt.date(year=2014, month=5, day=10),
        min_value=dt.date(year=1999, month=1, day=1),
        max_value=dt.date(year=2022, month=5, day=1))

choropleth=makeChoropleth(df[df.date == str(current_date)], -1, 50,'interest rate', "sunset", 
              "Interest Rate (%)", '<b>Central Bank Policy Rates by country</b>',
              'Source: BIS: Central Bank Policy Rates (https://www.bis.org/statistics/cbpol.htm)')


st.plotly_chart(choropleth)
# values = st.slider('Select a range of values', 0.0, 100.0, (25.0, 75.0))

format = 'MMM DD, YYYY'  # format output


# slider = cols1.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
