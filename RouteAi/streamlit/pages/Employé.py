import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
import geopy
import folium
from streamlit_folium import folium_static
import pgeocode
from PIL import Image
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
    page_title="RoutAi - Interface Employé",

    page_icon=logo,
    initial_sidebar_state="collapsed"
)

ms = st.session_state
if "themes" not in ms: 
  ms.themes = our_theme
  

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
st.subheader('Interface employé')
st.image(Image.open('RouteAi/streamlit/static/images/Ville-de-Gatineau.jpg'), width=100)


# Initialiser la base de données
if not os.path.exists('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE nids_de_poule (id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, code_postal TEXT, type_route TEXT, message TEXT, photo BLOB, localisation TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()


#lire donnes de la base de donnees data.db

    # Connexion à la base de données SQLite
conn = sqlite3.connect('data.db')
df = pd.read_sql('SELECT * FROM nids_de_poule', conn)
conn.close()
   
####################
# Transformer les données (still in progress)

area_weights = {
    'Artère Principale': 1,
    'Rue Collectrice': .6,
    'Rue Locale': .3
}


def transform_data(df):
    transformed_df = df.copy()
    weight_conf = .7
    weight_area = .3

    # Calculer l'indice de priorité
    transformed_df['IP_'] = (transformed_df['Indice_conf'] * weight_conf) + (transformed_df['type_route'].map(area_weights) * weight_area)
    #Change format of IP to %
    transformed_df['IP'] = transformed_df['IP_'].apply(lambda x: f"{x:.0%}")

    transformed_df = transformed_df.sort_values(by=['IP_', "created_at"], ascending=False)


    
    return transformed_df 
####################


df = transform_data(df)

tab1, tab2, tab3 = st.tabs(["🗺️ Carte", "📈 Tableau de bord", "🗃 Données"]) 


# Afficher les localisations des nids de poule signalés en utilisant folium
nomi = pgeocode.Nominatim('ca')
df['latitude'] = [nomi.query_postal_code(code).latitude for code in df['code_postal']]
df['longitude'] = [nomi.query_postal_code(code).longitude for code in df['code_postal']]

# Create a map centered around Gatineau
map = folium.Map(location=[45.4768, -75.7013], zoom_start=11, tiles="OpenStreetMap")

color_dict = {
   "Artère Principale": "red",
    "Rue Collectrice": "orange",
    "Rue Locale": "yellow"
}

# Add pothole locations
for i, row in df.iterrows():
    popup_content = f"#{row['id']} | {row['adresse']} | Indice IP : {row['IP']}"
    popup = folium.Popup(popup_content, max_width=1000)  # Adjust max_width to your preference
    folium.Marker([row['latitude'], row['longitude']], popup=popup, icon=folium.Icon(color=color_dict.get(row["type_route"], "yellow"), icon="info-sign")).add_to(map)


with tab1:
    # Display the map
    st.write('Localisation des nids de poule signalés')
    folium_static(map)

    # Ajouter des indication pour les couleurs des types de routes
    st.container()
    colors_emoji = {
        "Artère Principale": "🔴",
         "Rue Collectrice": "🟠",
        "Rue Locale": "🟡"
    }
    

    col1, col2, col3 = st.columns(3)
    for col, (key, value) in zip([col1, col2, col3], colors_emoji.items()):
        col.write(f"{value} {key}")


with tab2:
   # Create card with dropdown to decide which pothole to display
    st.write('Sélectionnez un nid de poule pour voir plus de détails')
    # Create dropdown to select pothole
    pothole_id = st.selectbox('Sélectionnez un nid de poule', df['id'])
    pothole = df[df['id'] == pothole_id].iloc[0]
    st.metric('Indice de priorité (et importance relative au seuil moyen)', pothole['IP'], delta= f"{pothole['IP_']-.6:.0%}", delta_color="inverse")

    st.data_editor((df
            
            .query(f'`id` == @pothole_id')
            .set_index('id')
            .drop(columns = [ 'photo','localisation', 'Indice_conf', 'IP_'])
            .rename(columns = {
                'id' : 'Identifiant',
                'adresse' : 'Adresse',
                'code_postal' : 'Code Postal',
                'type_route' : 'Type de route',
                'message' : 'Message',
                'created_at' : 'Date de signalement',
                })))
    



    # Assuming 'pothole' is the DataFrame row containing the BLOB data
    image_data = pothole['photo']  # This is the BLOB data from the database

    try:
        # Convert BLOB data to an image
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption='Photo du nid de poule', use_column_width=True)
    except Exception as e:
        st.error("Failed to load image from BLOB data.")
        st.write(str(e))


    # st.write(f"Adresse: {pothole['adresse']}")
    # st.write(f"Code Postal: {pothole['code_postal']}")
    # st.write(f"Type de route: {pothole['type_route']}")
    # st.write(f"Message: {pothole['message']}")
    # st.write(f"Date de signalement: {pothole['created_at']}")
    # Add 

with tab3:
    # Display a chart
    st.data_editor((df
          .set_index('id')
          .drop(columns = [ 'photo','localisation', 'Indice_conf', 'IP_'])
          .rename(columns = {
              'id' : 'Identifiant',
                'adresse' : 'Adresse',
                'code_postal' : 'Code Postal',
                'type_route' : 'Type de route',
                'message' : 'Message',
                'created_at' : 'Date de signalement',
                })),
                column_config={
        "photo": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        )
    },
    hide_index=False,

                )
    
    with st.form('delete-data'):
        st.write('Supprimer un nid de poule')
        pothole_id = st.selectbox(
   "Quel nid de poule voulez-vous supprimer ?",
    df['id'],
   index=None,
   placeholder="Selectionnez un nid de poule..",
)
        if st.form_submit_button('Supprimer'):
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f'DELETE FROM nids_de_poule WHERE id = {pothole_id}')
            conn.commit()
            conn.close()
            st.success('Nid de poule supprimé avec succès')

# Add buttons to return to the home page or view the reported potholes
st.markdown('---')
row = st.columns(2)
for col, emoji, title, link in zip(row, ["🏠", "👤"], ["Accueil", "Interface Client"], ["http://localhost:8501/Accueil", "http://localhost:8501/Citoyen"]):
    tile = col.container(height=170)
    tile.title(emoji)
    tile.link_button(title, link, )