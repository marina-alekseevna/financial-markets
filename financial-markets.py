import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime as dt
from datetime import datetime, date, time
from src.charts import makeChoropleth
import plotly.graph_objects as go

from src.utils import countries_cpi_ir_data

st.set_page_config(
        page_title="Financial Markets",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )

st.header("Official Date Picker")
select_year,select_month, select_countries = st.columns((1,1,4))

with select_year:
  st.write("\n\n\n")
  year = st.selectbox(
     'Select year',
     range(1999, 2023))

with select_month:
  st.write("\n\n\n")
  if year < 2022:
    month = st.selectbox(
      'Select month',
      range(1,13))
  else:
    month = st.selectbox(
      'Select month',
      range(1,5))
  
df = pd.read_csv(countries_cpi_ir_data)
all_countries = tuple(df.name.unique())
with select_countries:
  st.write("\n\n\n")
  symbols = st.multiselect("Choose countries", all_countries, 
    ("UK", "Germany", "Russian Federation", "Japan", "France", "USA", "Australia"))

graph1, graph2 = st.columns((1,1))

with graph1:
  choropleth1=makeChoropleth(df[(df.year == year)&(df.month == month)], -1, 50,'InterestRate', "sunset", 
              "Interest Rate (%)", '<b>Central Bank Policy Rates</b>',
              'Source: BIS: Statistics (https://www.bis.org/statistics/full_data_sets.htm)')


  st.plotly_chart(choropleth1, use_container_width=True)
with graph2:
  choropleth2=makeChoropleth(df[(df.year == year)&(df.month == month)], -1, 50,'CPI', "sunset", 
              "CPI (%)", '<b>Consumer Price Index Change</b>',
              'Source: BIS: Statistics (https://www.bis.org/statistics/full_data_sets.htm)')


  st.plotly_chart(choropleth2, use_container_width=True)
with graph3:
  pass