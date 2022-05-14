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

graph1, graph2, graph3 = st.columns((1,1,1))

with graph1:
  choropleth1=makeChoropleth(df[(df.year == year)&(df.month == month)], -1, 50,'InterestRate', "sunset", 
              "Interest Rate (%)", '<b>Central Bank Policy Rates</b>',
              'Source: BIS: Statistics (https://www.bis.org/statistics/full_data_sets.htm)')


  st.plotly_chart(choropleth1)
with graph2:
  choropleth2=makeChoropleth(df[(df.year == year)&(df.month == month)], -1, 50,'CPI', "sunset", 
              "CPI (%)", '<b>Consumer Price Index Change</b>',
              'Source: BIS: Statistics (https://www.bis.org/statistics/full_data_sets.htm)')


  st.plotly_chart(choropleth2)
with graph3:
  pass
# values = st.slider('Select a range of values', 0.0, 100.0, (25.0, 75.0))

format = 'MMM DD, YYYY'  # format output


# slider = cols1.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
start_color, end_color = st.select_slider(
     'Select a range of color wavelength',
     options=['1999-01', '1999-02', '1999-03', '1999-04', '1999-05', '1999-06',
       '1999-07', '1999-08', '1999-09', '1999-10', '1999-11', '1999-12',
       '2000-01', '2000-02', '2000-03', '2000-04', '2000-05', '2000-06',
       '2000-07', '2000-08', '2000-09', '2000-10', '2000-11', '2000-12',
       '2001-01', '2001-02', '2001-03', '2001-04', '2001-05', '2001-06',
       '2001-07', '2001-08', '2001-09', '2001-10', '2001-11', '2001-12',
       '2002-01', '2002-02', '2002-03', '2002-04', '2002-05', '2002-06',
       '2002-07', '2002-08', '2002-09', '2002-10', '2002-11', '2002-12',
       '2003-01', '2003-02', '2003-03', '2003-04', '2003-05', '2003-06',
       '2003-07', '2003-08', '2003-09', '2003-10', '2003-11', '2003-12',
       '2004-01', '2004-02', '2004-03', '2004-04', '2004-05', '2004-06',
       '2004-07', '2004-08', '2004-09', '2004-10', '2004-11', '2004-12',
       '2005-01', '2005-02', '2005-03', '2005-04', '2005-05', '2005-06',
       '2005-07', '2005-08', '2005-09', '2005-10', '2005-11', '2005-12',
       '2006-01', '2006-02', '2006-03', '2006-04', '2006-05', '2006-06',
       '2006-07', '2006-08', '2006-09', '2006-10', '2006-11', '2006-12',
       '2007-01', '2007-02', '2007-03', '2007-04', '2007-05', '2007-06',
       '2007-07', '2007-08', '2007-09', '2007-10', '2007-11', '2007-12',
       '2008-01', '2008-02', '2008-03', '2008-04', '2008-05', '2008-06',
       '2008-07', '2008-08', '2008-09', '2008-10', '2008-11', '2008-12',
       '2009-01', '2009-02', '2009-03', '2009-04', '2009-05', '2009-06',
       '2009-07', '2009-08', '2009-09', '2009-10', '2009-11', '2009-12',
       '2010-01', '2010-02', '2010-03', '2010-04', '2010-05', '2010-06',
       '2010-07', '2010-08', '2010-09', '2010-10', '2010-11', '2010-12',
       '2011-01', '2011-02', '2011-03', '2011-04', '2011-05', '2011-06',
       '2011-07', '2011-08', '2011-09', '2011-10', '2011-11', '2011-12',
       '2012-01', '2012-02', '2012-03', '2012-04', '2012-05', '2012-06',
       '2012-07', '2012-08', '2012-09', '2012-10', '2012-11', '2012-12',
       '2013-01', '2013-02', '2013-03', '2013-04', '2013-05', '2013-06',
       '2013-07', '2013-08', '2013-09', '2013-10', '2013-11', '2013-12',
       '2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06',
       '2014-07', '2014-08', '2014-09', '2014-10', '2014-11', '2014-12',
       '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06',
       '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12',
       '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06',
       '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
       '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06',
       '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12',
       '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06',
       '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
       '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
       '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
       '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06',
       '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
       '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06',
       '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
       '2022-01', '2022-02', '2022-03'],
     value=('2019-07', '2021-01'))

symbols = st.multiselect("Choose stocks to visualize", df.ISO3.unique(),  df.ISO3.unique()[:5])

st.write("a logo and text next to eachother")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.write("Hi")

with col2:
    st.write('A Name')

a = st.sidebar.radio('Select one:', [1, 2])