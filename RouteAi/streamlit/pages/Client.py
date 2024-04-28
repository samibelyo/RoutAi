import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
from streamlit_geolocation import streamlit_geolocation
import datetime

st.title('RoutAi')
st.subheader('Interface client')

st.write('Veuillez remplir le formulaire ci-dessous pour signaler un nid de poule')

# Initialiser la base de données
if not os.path.exists('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

with st.form(key='my_form'):
    # Créer formulaire à remplir
    adresse = st.text_input('Adresse')
    code_postal = st.text_input('Code Postal')
    type_route = st.selectbox('Type de route', ['Artère Principale', 'Rue Collectrice'
    , 'Rue Locale'])
    message = st.text_area('Message')
    # Photo est obligatoire

    photo = st.file_uploader('Photo du nid de poule (Obligatoire)', type=['jpg', 'jpeg', 'png'])

    # localisation = streamlit_geolocation()
    localisation = np.nan


    submitted = st.form_submit_button('Soumettre')



    if submitted:

        if photo is not None:
            photo_data = photo.read()
        else:
            st.error('Veuillez ajouter une photo du nid de poule')
            st.stop()

        # Enregistrer les données dans la base de données
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT, created_at TIMESTAMP)''')
        current_time = datetime.datetime.now()
        c.execute('INSERT INTO nids_de_poule (adresse, code_postal, type_route, message, photo, localisation, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)', (adresse, code_postal, type_route, message, photo_data, localisation, current_time))
        conn.commit()
        conn.close()
        st.success('Nid de poule signalé avec succès')

