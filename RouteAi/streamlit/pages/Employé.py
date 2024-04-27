import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3


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
