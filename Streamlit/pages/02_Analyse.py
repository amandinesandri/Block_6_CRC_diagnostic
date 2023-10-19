import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="CRC_Diag",
    page_icon="2286253.png",
    layout="wide",
)

st.subheader('Analyse du dataframe')

if 'data' in st.session_state:
    df = st.session_state.data

    st.header("Répartition des patients en fonction de leur état de santé")
    fig = px.histogram(df, x='condition')
    st.plotly_chart(fig)

    df_CRC= df[df['condition']=='CRC']
    df_CRC1= df_CRC.drop(columns=['condition'], axis=1)
    df_grouped_CRC= df_CRC1.groupby('country',axis=0).mean()

    df_CTRL= df[df['condition']=='control']
    df_CTRL1= df_CTRL.drop(columns=['condition'], axis=1)
    df_grouped_CTRL= df_CTRL1.groupby('country',axis=0).mean()

    def generate_plot(selected_df, selected_country):
        country_data = selected_df.loc[selected_country]
        temp_df = pd.DataFrame({'bacteria': country_data.index, 'mean_quantity': country_data.values})
        fig = px.treemap(temp_df, path=['bacteria'], values='mean_quantity', title=f"Microbiota composition in {selected_country}")
        st.plotly_chart(fig)
    
    selected_df= None
    selected_country = None

    st.header("Composition du microbiome en fonction de l'état de santé du patient et de son pays")
    selection = st.selectbox('Sélection de condition de santé', ('Patients sains', 'Patients atteint du CRC'))
    if selection =="Patients sains":
        selected_df = df_grouped_CTRL
    else:
        selected_df = df_grouped_CRC
    
    if selected_df is not None:
        selected_country = st.selectbox("Sélectionnez un pays:", selected_df.index.tolist())
        generate_plot(selected_df, selected_country)
    else:
        st.warning("Sélectionnez d'abord une condition (Patients sains ou Patients atteints du CRC)")
    
    st.write("Les pavés colorés représentent, dans l'ordre décroissant, la quantité moyenne pour chaque bactérie pour chaque status de santé et pour chaque pays.")