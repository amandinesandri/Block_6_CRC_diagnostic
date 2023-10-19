import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CRC_Diag",
    page_icon="2286253.png",
    layout="wide",
)

st.subheader('Load Data')

if 'data' in st.session_state:
    df = st.session_state.data

    if st.checkbox("Show Data"):
        st.subheader('Raw data')
        st.write(df)
    else:
        st.warning("Data not loaded yet. Please visit the Home page first.")