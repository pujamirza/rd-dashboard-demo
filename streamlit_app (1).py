import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="R&D Dashboard", layout="wide")
st.title("🔬 R&D Resource & Portfolio Dashboard")

# Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

# Load the Sheet
sheet = client.open_by_key("11CMb-1x9YDA1kh0ihdPb7PUpnb5hsDXPWbVMK7PtDSU")

# Define worksheet names
tabs = {
    "📋 Project List": "Portfolio DB",
    "👥 Resource List": "R&D Resource DB",
    "📊 Allocations – ONC": "ONC",
    "📊 Allocations – WH": "WH",
    "📊 Allocations – OH": "OH",
    "📊 Allocations – XBU": "XBU",
    "📊 Allocations – ECD": "ECD"
}

tab_objs = st.tabs(list(tabs.keys()))
for i, (tab_label, sheet_name) in enumerate(tabs.items()):
    with tab_objs[i]:
        st.subheader(f"{tab_label}")
        try:
            data = sheet.worksheet(sheet_name).get_all_records()
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ Could not load '{sheet_name}': {e}")
