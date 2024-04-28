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

logo = Image.open('RouteAi/streamlit/static/images/transparent.png')
st.set_page_config(
    page_title="RoutAi - Interface Employé",

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
st.subheader('Interface employé')

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
    'Rue Collectrice': .8,
    'Rue Locale': .66
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



# Add buttons to return to the home page or view the reported potholes
st.markdown('---')
row = st.columns(2)
for col, emoji, title, link in zip(row, ["🏠", ":warning:"], ["Accueil", "Interface Client"], ["http://localhost:8501/Accueil", "http://localhost:8501/Client"]):
    tile = col.container(height=170)
    tile.title(emoji)
    tile.link_button(title, link, )