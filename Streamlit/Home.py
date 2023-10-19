import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CRC_Diag",
    page_icon="2286253.png",
    layout="wide",
)


def main():
    st.header("HOME PAGE")
    st.title("🔬 CRC_Diag 👩🏻‍🔬")
    choix = st.sidebar.radio("SubMenu", ["Description", "Documentation"])
    if choix == "Description":
        st.subheader("Est il possible d’utiliser la composition du microbiote pour détecter le cancer colorectal")

        st.write("Le microbiote intestinal : un rôle dans la détection du cancer colorectal.")
        st.write("Cette application a été développée pour répondre à un besoin crucial en matière de santé publique :")
        st.write("la détection précoce du cancer colorectal, troisième cancer le plus meurtrier.")
        st.write("Le cancer colorectal est une pathologie touchant, comme son nom l'indique, le côlon (partie moyenne du gros intestin,")
        st.write("entre le cæcum et rectum) ou le rectum (dernière partie du gros intestin).")
        st.write("Cette maladie, lorsqu'elle est détectée tardivement, peut être mortelle.")
        st.write("Les chances de guérison du cancer colorectal sont en effet directement corrélées à son stade de progression au diagnostic.")
        st.write("Le microbiote intestinal regroupe des milliers de milliards de micro-organismes( bactéries, levures et virus)")
        st.write("vivant principalement dans les intestins et en symbiose avec l’organisme.")
        st.write("Le microbiote va permettre au système immunitaire d’apprendre à faire la différence entre les microorganismes « amis » et les pathogènes.")
        st.write("Des études ont montré qu’un déséquilibre du microbiote intestinal, appelé « dysbiose », favorisait la survenue d’un cancer du côlon.")
        st.write("Ce dashboard offre un outil interactif pour explorer ces relations complexes.")
        st.write("Son objectif principal  est de fournir à ses utilisateurs une interface intuitive pour analyser et")
        st.write("interpréter les données du microbiote intestinal en relation avec le cancer colorectal.")

    if choix == "Documentation":
        st.subheader("Voici la documentation de l'application web")

        
    @st.cache_data
    def load_data():
        data = pd.read_csv("/home/app/pages/Microbiota_composition.csv")           
        return data
    if 'data' not in st.session_state:
        st.session_state.data = load_data()





if __name__ == "__main__":
    main()