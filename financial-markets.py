import streamlit as st
import pandas as pd
import numpy as np

st.title('Financial Markets')

import time
import datetime as dt

from datetime import datetime, date, time

st.header("Official Date Picker")
st.date_input('start date')
st.date_input('end date')

values = st.slider('Select a range of values', 0.0, 100.0, (25.0, 75.0))

cols1,_ = st.columns((1,2)) # To make it narrower
format = 'MMM DD, YYYY'  # format output
start_date = dt.date(year=2021,month=1,day=1)-relativedelta(years=2)  #  I need some range in the past
end_date = dt.datetime.now().date()-dt.relativedelta(years=2)
max_days = end_date-start_date

slider = cols1.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
## Sanity check
st.table(pd.DataFrame([[start_date, slider, end_date]],
                columns=['start',
                        'selected',
                        'end'],
                index=['date']))