import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="CRC_Diag",
    page_icon="2286253.png",
    layout="wide",
)


#def page_1():
st.title("🔬 CRC_Diag 👩🏻‍🔬")

st.markdown("""##`Outil de diagnostic du Cancer Colorectal à partir de la composition du microbiote intestinal`""")
st.markdown("""###`Dans cette application web, vous aurez en première page un dashboard`""")
st.markdown("""###`En page deux, vous aurez `""")


st.markdown("Check out data here: [Data on the daily number of new reported COVID-19 cases and deaths by EU/EEA country](https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country)")
st.caption("At the moment of this app, data was lastly collected on December 25th 2021")
@st.cache
def load_data():
    data = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv")      
    return data