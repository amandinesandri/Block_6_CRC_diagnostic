import io
import pandas as pd
import streamlit as st
import requests
# api.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
import shutil
import pickle
import os
import uvicorn
import logging

st.title("Uploadez un fichier CSV avec Streamlit et FastAPI")

uploaded_file = st.file_uploader("Uploader un fichier CSV", type=["csv"])

if uploaded_file:
    st.write("Fichier uploadé avec succès!")
    st.write("Nom du fichier:", uploaded_file.name)
    df = pd.read_csv(uploaded_file)

    # Affichez le DataFrame dans Streamlit
    st.write("Voici le dataframe:")
    st.write(df)

    # Sélection de la ligne pour la prédiction
    selected_row = st.number_input("Sélectionnez l'indice de la ligne à prédire (0 à {}):".format(len(df)-1), min_value=0, max_value=len(df)-1)

    if st.button("Effectuer la prédiction"):
        if 0 <= selected_row < len(df):
            # Convertissez le DataFrame en texte CSV
            csv_data = df.to_csv(index=False)

            # Créez un objet BytesIO à partir du texte CSV
            csv_file = io.BytesIO(csv_data.encode())
            # Appel à l'API FastAPI pour la prédiction sur une seule ligne
            response = requests.post(f"http://localhost:4000/predict/{selected_row}", files={"file": ("data.csv", csv_file)})

            # st.write(response)

            if response.status_code == 200:
                result = response.json()
                pred = result["predictions"][0]
                # if pred = 0, pred = "Sain", else pred = "CRC"
                if pred == 0:
                    st.write("Prédiction sur la condition du patient sélectionné:", " Sain")
                else:
                    st.write("Prédiction sur la condition du patient sélectionné:", " CRC")
                # st.write("Prédiction sur la condition du patient sélectionné:", result["predictions"][0])
                # st.write("Prédiction sur la condition du patient sélectionné:", pred)
                # st.write(result["predictions"][0])
            else:
                st.write("Erreur lors de la prédiction. Veuillez réessayer.")
                print(response.json())

        else:
            st.write("Indice de ligne invalide. Veuillez sélectionner un indice valide.")

# if uploaded_file:
#     st.write("Fichier uploadé avec succès!")
#     st.write("Nom du fichier:", uploaded_file.name)
#     df = pd.read_csv(uploaded_file)

#     files = {"file": uploaded_file}
#     response = requests.post("http://localhost:4000/uploadfile/", files=files)
#     # st.write("Réponse du serveur FastAPI:")
#     # st.write(response.json())
    

#     if st.button("Effectuer la prédiction"):
#         # Créez un dataframe pandas à partir du fichier téléchargé
#         st.write("Voici le dataframe:")
#         st.write(df)

#         # Convertissez le DataFrame en texte CSV
#         csv_data = df.to_csv(index=False)

#         # Créez un objet BytesIO à partir du texte CSV
#         csv_file = io.BytesIO(csv_data.encode())

#         # Envoi du dataframe à FastAPI pour la prédiction
#         response = requests.post("http://localhost:4000/predict/", files={"file": ("data.csv", csv_file)})

#         if response.status_code == 200:
#             result = response.json()
#             # st.write(result)
#             st.write("Prédictions:")
#             st.write(pd.DataFrame(result["predictions"], columns=["Prediction"]))
#         else:
#             st.write("Erreur lors de la prédiction. Veuillez réessayer.")

######## API #########

app = FastAPI()

# Spécifiez le chemin complet du dossier cible
UPLOAD_FOLDER = "uploads"

MODEL_FILE = "xgboost_classifier_model.pkl"

# Chargez le modèle pré-entraîné
with open(MODEL_FILE, "rb") as model_file:
    model = pickle.load(model_file)

# Chargez le scaler (StandardScaler) pré-entraîné si nécessaire
# Assurez-vous que le scaler est compatible avec le modèle
SCALER_FILE = "scaler.pkl"
with open(SCALER_FILE, "rb") as scaler_file:
    scaler = pickle.load(scaler_file)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    # Assurez-vous que le dossier cible existe, s'il n'existe pas, créez-le
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename}

@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        # Assurez-vous que le dossier cible existe, s'il n'existe pas, créez-le
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Chargez les données du fichier CSV
        data = pd.read_csv(file_path)

        if data is None:
            return {"error : dataframe is none"}
        
        data = data.drop(columns=["country"], axis=1)
        
        # Appliquez la mise à l'échelle avec le StandardScaler
        if scaler is not None:
            data = scaler.transform(data)
        
        # Effectuez la prédiction en utilisant le modèle
        predictions = model.predict(data)  # Assurez-vous que votre modèle peut effectuer des prédictions sur les données fournies
        
        # Vous pouvez renvoyer les prédictions au format JSON ou tout autre format souhaité
        return {"predictions": predictions.tolist()}
    except Exception as e:
        return {"error": str(e)}


@app.post("/predict/{row_index}")
async def predict_row(row_index: int, file: UploadFile):
    try:
        # Assurez-vous que le dossier cible existe, s'il n'existe pas, créez-le
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Chargez les données du fichier CSV
        data = pd.read_csv(file_path)
        data = data.drop(columns=["country"], axis=1)

        if data is None:
            return {"error": "Le DataFrame est vide."}
        
        # Vérifiez si l'indice de la ligne est valide
        if row_index < 0 or row_index >= len(data):
            return {"error": "Index de ligne invalide."}

        # Sélectionnez la ligne à partir du DataFrame
        row = data.iloc[[row_index]]

        # Appliquez la mise à l'échelle avec le StandardScaler
        if scaler is not None:
            row = scaler.transform(row)
        
        # Effectuez la prédiction en utilisant le modèle
        prediction = model.predict(row)  # Assurez-vous que votre modèle peut effectuer des prédictions sur une seule ligne de données
        
        # Inclure la clé "predictions" dans la réponse JSON
        return {"predictions": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)

