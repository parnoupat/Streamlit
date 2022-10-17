import pandas as pd
import streamlit as st
from pandas import DataFrame
# import google_auth_httplib2
# import httplib2

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = st.secrets["SPREADSHEET_ID"]
SHEET_NAME = st.secrets["SHEET_NAME"]
SHEET_RANGE = "!A:C"
# GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
GSHEET_URL = st.secrets["private_gsheets_url"]


# from gsheetsdb import connect

# Create a connection object.
# conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
# def run_query(query):
#     rows = conn.execute(query, headers=1)
#     rows = rows.fetchall()
#     return rows

# sheet_url = st.secrets["private_gsheets_url"]
# rows = run_query(f'SELECT * FROM "{sheet_url}"')


@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}{SHEET_RANGE}",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}{SHEET_RANGE}",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()





gsheet_connector = connect_to_gsheet()

#Form Beginning
def clear_form():
    st.session_state["ชื่อ-สกุล"] = ""
    st.session_state["เบอร์โทรศัพท์"] = ""
form = st.form(key="annotation")
with form:
    st.title('ทดสอบลงทะเบียน LIFF')
    st.subheader('Test LIFF')
    name = st.text_input('✍️ชื่อ-สกุล',key='ชื่อ-สกุล')
    gender = st.radio('เพศ',('ชาย','หญิง'))
    telephone = st.text_input('เบอร์โทรศัพท์',key='เบอร์โทรศัพท์')
    submitted = st.form_submit_button(label="Submit")
    clear = st.form_submit_button(label="Clear", on_click=clear_form)


if submitted:
    datalist = [[name,
        gender,
        telephone]]
    add_row_to_gsheet(gsheet_connector,datalist)

expander = st.expander("See all records")
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))