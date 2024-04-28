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
import io

our_theme = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "#1B1B1B",
                              "theme.primaryColor": "#c98bdb",
                              "theme.secondaryBackgroundColor": "#5591f5",
                              "theme.textColor": "white",
                              "theme.textColor": "white",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "#5591f5",
                              "theme.secondaryBackgroundColor": "#F6F6F6",
                              "theme.textColor": "#0a1464",
                              "button_face": "🌞"},
                    }
logo = Image.open('RouteAi/streamlit/static/images/transparent.png')
st.set_page_config(
    page_title="RoutAi",

    page_icon=logo,
    initial_sidebar_state="collapsed"
)
ms = st.session_state
if "themes" not in ms: 
  ms.themes = ms.themes = our_theme
  

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

# Database setup
DB_NAME = 'data.db'
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE nids_de_poule (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            adresse TEXT, 
            code_postal TEXT, 
            type_route TEXT, 
            message TEXT, 
            photo BLOB, 
            localisation TEXT,
            Indice_conf REAL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

init_db()



st.title('RoutAi - Interface Citoyen')

st.write('Si tu ne connais pas les différents types de routes, voici les voici :')

cols = st.columns(3)
for col, emoji, title, desc in zip(cols, ["🔴", "🟠", "🟡"], ["Artère Principale", "Rue Collectrice", "Rue Locale"], 
                              ["Route principale de la ville", "Route avec beaucoup de circulation.", "Route résidentielle"]):
    with col:
        with st.expander(emoji + " "+ title):
            st.write(desc)

# Form for pothole reporting
with st.form(key='pothole_form'):
    adresse = st.text_input('Adresse')
    code_postal = st.text_input('Code Postal')
    type_route = st.selectbox('Type de route', ['Artère Principale', 'Rue Collectrice', 'Rue Locale'])
    message = st.text_area('Message')
    uploaded_file = st.file_uploader("Insérez une photo du nid de poule", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button('Submit')

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

    
    if uploaded_file:
        photo=preprocess_image(Image.open(uploaded_file))
        #st.image(photo)
        prediction = make_prediction(photo)
        indice=prediction.boxes.conf
    # st.header("indice de priorite")
        list_indice=[]
        for value in indice:
            list_indice.append(value.item()) 
        if len(list_indice) > 0:
            max_value = max(list_indice)
        else:
            max_value=0



    if submitted:
        if uploaded_file is not None:
            # Convert the uploaded file to an image and save it as a BLOB
            image = Image.open(uploaded_file)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Save to SQLite database
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''INSERT INTO nids_de_poule (adresse, code_postal, type_route, message, photo, localisation, Indice_conf, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (adresse, code_postal, type_route, message, img_byte_arr, None, max_value, datetime.datetime.now()))
            conn.commit()
            conn.close()
            st.success('Pothole reported successfully!')
        else:
            st.error('Please upload a photo of the pothole.')


# Add buttons to return to the home page or view the reported potholes
st.markdown('---')
row = st.columns(2)
for col, emoji, title, link in zip(row, ["🏠", ":construction:"], ["Accueil", "Interface Employé"], ["http://localhost:8501/Accueil", "http://localhost:8501/Employé"]):
    tile = col.container(height=170)
    tile.title(emoji)
    tile.link_button(title, link, )