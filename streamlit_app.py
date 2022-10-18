from lib2to3.pgen2.grammar import opmap_raw
import pandas as pd
import streamlit as st
from pandas import DataFrame
import google_auth_httplib2
import httplib2
import streamlit as st
import streamlit.components.v1 as components
import logging
import pathlib
import shutil

from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from streamlit.components.v1 import html
from streamlit_javascript import st_javascript

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


with open("index.html") as f:
    st.markdown(f'<body>{f.read()}</body>',unsafe_allow_html=True)
    return_value3 = st_javascript(f.read())
    st.markdown(f"Return value was: {return_value3}")
    components.iframe(f.read())



LIFF_JS = """
<script src="https://static.line-scdn.net/liff/edge/versions/2.9.0/sdk.js"></script>
"""

index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
logging.info(f'editing {index_path}')
soup = BeautifulSoup(index_path.read_text(), features="html.parser")
htmls = str(soup)
new_html = htmls.replace('<head>', '<head>\n' + LIFF_JS)
index_path.write_text(new_html)



st.header("test html import")

html_string = '''
<h1>HTML string in RED</h1>
  <img id="pictureUrl" width="25%">
  <p id="userId"></p>
  <p id="displayName"></p>
  <p id="statusMessage"></p>
  <p id="getDecodedIDToken"></p>

<script src="https://static.line-scdn.net/liff/edge/versions/2.9.0/sdk.js"></script>
<script language="javascript">
  function runApp() {
    liff.getProfile().then(profile => {
      document.getElementById("pictureUrl").src = profile.pictureUrl;
      document.getElementById("userId").innerHTML = '<b>UserId:</b> ' + profile.userId;
      document.getElementById("displayName").innerHTML = '<b>DisplayName:</b> ' + profile.displayName;
      document.getElementById("statusMessage").innerHTML = '<b>StatusMessage:</b> ' + profile.statusMessage;
      document.getElementById("getDecodedIDToken").innerHTML = '<b>Email:</b> ' + liff.getDecodedIDToken().email;
    }).catch(err => console.error(err));
    return profile.displayName
  }
  liff.init({ liffId: "1657566121-pOJyJlDk" }, () => {
    if (liff.isLoggedIn()) {
      runApp()
    } else {
      liff.login();
    }
  }, err => console.error(err.code, error.message));
</script>
<script language="javascript">
   document.querySelector("h1").style.color = "red";
   console.log("Streamlit runs JavaScript");
   alert("Streamlit runs JavaScript");
</script>
'''

components.html(html_string)

HtmlFile = open("testLIFF.html")
Boostrap = open("Boostrap_script.html")
components.html("""<head><script src="https://static.line-scdn.net/liff/edge/versions/2.9.0/sdk.js"></script></head>""",height=600,)
components.html(HtmlFile.read(),height=600,)
components.html(Boostrap.read(),height=600,)

js_code = """await fetch("/testLIFF_code.html").then(function(response) {return response.json();})"""

test_js_code = """
function myFunction(name) {
  return "Hello " + name;
}
myFunction("parnoupat")
"""


return_value2 = st_javascript(js_code)

return_value = st_javascript("""

liff.init({ liffId: "1657566121-pOJyJlDk" }, () => {
    if (liff.isLoggedIn()) {
      liff.getProfile().then(profile => {
        const name = profile.displayName;
        return 3;
  })
  .catch((err) => {
    console.log("error", err);
  });
    } else {
      return 1;
    }
  }, err => console.error(err.code, error.message))
  """)

lineliff = st_javascript("""await fetch(liff.getProfile()).then(function(response) {
    return response.json();
})  """)

st.markdown(f"Return value was: {return_value3}")
print(f"Return value was: {return_value}")

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


# Define your javascript
my_js = """
alert("Hello JavaScript");
"""

# Wrapt the javascript as html code
my_html = f"<script>{my_js}</script>"

# Execute your app
st.title("Javascript example")
html(my_html)


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