import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
import geopy
import folium
from streamlit_folium import folium_static
import pgeocode


st.title('RoutAi')
st.subheader('Interface employé')

# Initialiser la base de données
if not os.path.exists('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

# Afficher les nids de poule signalés
conn = sqlite3.connect('data.db')
df = pd.read_sql('SELECT * FROM nids_de_poule', conn)
conn.close()

####################
# Transformer les données (still in progress)
def transform_data(df):
    df1 = df.copy()

transformed_df = df.copy()
####################

st.write((df
          .set_index('id')
          .drop(columns = ['photo', 'localisation'])
          .rename(columns = {
              'id' : 'Identifiant',
                'adresse' : 'Adresse',
                'code_postal' : 'Code Postal',
                'type_route' : 'Type de route',
                'message' : 'Message',
                'created_at' : 'Date de signalement'})))

# Afficher les localisations des nids de poule signalés en utilisant folium
nomi = pgeocode.Nominatim('ca')
df['latitude'] = [nomi.query_postal_code(code).latitude for code in df['code_postal']]
df['longitude'] = [nomi.query_postal_code(code).longitude for code in df['code_postal']]

# Create a map centered around Gatineau
map = folium.Map(location=[45.4768, -75.7013], zoom_start=12)

# Add pothole locations
for i, row in df.iterrows():
    popup_content = f"#{row['id']} | {row['adresse']} | INDICE : {np.random.randint(1, 100)}/100\n"
    popup = folium.Popup(popup_content, max_width=500)  # Adjust max_width to your preference
    folium.Marker([row['latitude'], row['longitude']], popup=popup, icon=folium.Icon(color="red", icon="info-sign")).add_to(map)

st.subheader('Localisation des nids de poule signalés')

# Display the map
folium_static(map)



