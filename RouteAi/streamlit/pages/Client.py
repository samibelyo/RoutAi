import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
from streamlit_geolocation import streamlit_geolocation
import datetime
from ultralytics import YOLO
import streamlit as st
from PIL import Image
import torch

logo = Image.open('RouteAi/streamlit/static/images/transparent.png')
st.set_page_config(
    page_title="RoutAi - Interface Client",

    page_icon=logo,
    initial_sidebar_state="collapsed"
)

ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "black",
                              "theme.primaryColor": "#c98bdb",
                              "theme.secondaryBackgroundColor": "#5591f5",
                              "theme.textColor": "white",
                              "theme.textColor": "white",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "#5591f5",
                              "theme.secondaryBackgroundColor": "#82E1D7",
                              "theme.textColor": "#0a1464",
                              "button_face": "🌞"},
                    }
  

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
# Put button on top right corner
cols = st.columns([1,1,1,1,1])
cols[-1].button(btn_face, on_click=ChangeTheme, )


if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()


st.title('RoutAi')
st.subheader('Interface client')

st.write('Veuillez remplir le formulaire ci-dessous pour signaler un nid de poule')

st.write('Si tu ne connais pas les différents types de routes, voici les voici :')

cols = st.columns(3)
for col, emoji, title, desc in zip(cols, ["🔴", "🟠", "🟡"], ["Artère Principale", "Rue Collectrice", "Rue Locale"], 
                              ["Route principale de la ville", "Route secondaire", "Route résidentielle"]):
    with col:
        with st.expander(emoji + " "+ title):
            st.write(desc)
    
    




# Initialiser la base de données
if not os.path.exists('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT,Indice_conf REAL , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

with st.form(key='my_form'):

    # Créer formulaire à remplir
    adresse = st.text_input('Adresse')
    code_postal = st.text_input('Code Postal')
    type_route = st.selectbox('Type de route', ['Artère Principale', 'Rue Collectrice', 'Rue Locale'])
    message = st.text_area('Message')
    # Photo est obligatoire


    # Load your trained YOLO model
    test_model = YOLO("best.pt", task="detect")

    ##fonction de preprocess 
    def preprocess_image(image, target_size=(640, 640)):
        if image.size == target_size:
            return image
        else:
            # Resize the image to the target size
            image = image.resize(target_size)
        return image

    ##fonction de prediction 
    def make_prediction(img): 
        prediction = test_model(img,conf=0.2)
        prediction = prediction[0]                ## Dictionary with keys "boxes", "labels", "scores".
        return prediction

    #photo = st.file_uploader('Photo du nid de poule (Obligatoire)', type=['jpg', 'jpeg', 'png'])
    upload = st.file_uploader(label="Upload Image :", type=["png", "jpg", "jpeg"]) ## Image as Bytes 
    if upload:
        photo=preprocess_image(Image.open(upload))
        #st.image(photo)
        prediction = make_prediction(photo)
        indice=prediction.boxes.conf
    # st.header("indice de priorite")
        list_indice=[]
        for value in indice:
            list_indice.append(value.item()) 
        if len(list_indice) > 0:
            max_value = max(list_indice)

            #st.write( max_value)
        else:
            max_value=None
            #st.write("Aucun nid de poule détecté.") 
            #st.write(None)   




    # localisation = streamlit_geolocation()
    localisation = np.nan

    submitted = st.form_submit_button('Soumettre')




    if submitted:

        if upload is not None:
            upload= upload.read()
        else:
            st.error('Veuillez ajouter une photo du nid de poule')
            st.stop()

        # Enregistrer les données dans la base de données
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT,Indice_conf REAL , created_at TIMESTAMP)''')
        current_time = datetime.datetime.now()
        c.execute('INSERT INTO nids_de_poule (adresse, code_postal, type_route, message, photo, localisation,Indice_conf, created_at) VALUES (?, ?, ?, ?, ?, ?, ?,?)', (adresse, code_postal, type_route, message, upload, localisation,max_value ,current_time))
        conn.commit()
        conn.close()
        st.success('Nid de poule signalé avec succès')

# Add buttons to return to the home page or view the reported potholes
st.markdown('---')
row = st.columns(2)
for col, emoji, title, link in zip(row, ["🏠", ":construction:"], ["Accueil", "Interface Employé"], ["http://localhost:8501/Accueil", "http://localhost:8501/Employé"]):
    tile = col.container(height=170)
    tile.title(emoji)
    tile.link_button(title, link)