import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
from streamlit_geolocation import streamlit_geolocation

st.title('RoutAi')
st.subheader('Interface client')

st.write('Veuillez indiquer votre position pour signaler un nid de poule')
st.write('Vous pouvez également ajouter une photo du nid de poule')
st.write('Veuillez remplir le formulaire ci-dessous')

# Initialiser la base de données
if not os.path.exists('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

# Créer formulaire à remplir
adresse = st.text_input('Adresse')
code_postal = st.text_input('Code Postal')
type_route = st.selectbox('Type de route', ['Artère Principale', 'Rue Collectrice'
, 'Rue Locale'])
message = st.text_area('Message')
photo = st.file_uploader('Photo du nid de poule', type=['jpg', 'jpeg', 'png'])

# localisation = streamlit_geolocation()
localisation = np.nan






if st.button('Soumettre'):
    # Enregistrer les données dans la base de données
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT)''')
    c.execute('INSERT INTO nids_de_poule (adresse, code_postal, type_route, message, photo, localisation) VALUES (?, ?, ?, ?, ?, ?)', (adresse, code_postal, type_route, message, photo.read(), localisation))
    conn.commit()
    conn.close()
    st.success('Nid de poule signalé avec succès')

