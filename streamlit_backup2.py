import pandas as pd
import numpy as np
import streamlit as st
from pandas import DataFrame


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
# streamlit_app.py

from gspread_pandas import Spread,Client
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope,)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "Streamlit DB"
spread = Spread(spreadsheetname,client = client) 
conn = connect(credentials=credentials)

# Check the connection
st.write(spread.url)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["gsheets"]["Sheet1"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
# for row in rows:
#    st.write(f"{row.name} has a :{row.pet}:")

"""
# My first app
Here's our first attempt at using data to create a table:
"""

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)


x = st.slider('x')

st.write(x, 'squared is', x * x)
st.text_input("Your name", key="name")
st.session_state.name
