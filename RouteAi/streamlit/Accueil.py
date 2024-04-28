import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

logo = Image.open('RouteAi/streamlit/static/images/transparent.png')
st.set_page_config(
    page_title="RoutAi",

    page_icon=logo,
)

st.image(logo, width=200)
st.title('RoutAi')
#show logo

st.subheader('Une application simple pour reporter les nids de poule')

# Add separator
st.markdown('---')

# Add title
st.header('Choisissez votre profil')
row = st.columns(2)
#
for col, emoji, title, link in zip(row, [" :warning:", ":construction:"], ["Interface Client", "Interface Employé"], ["http://localhost:8501/Client", "http://localhost:8501/Employé"]):
    tile = col.container(height=170)
    tile.title(emoji)
    tile.markdown(f"[{title}]({link})", unsafe_allow_html=True)




st.markdown(
    """
    ### Description
    RoutAi est une application qui permet aux citoyens de signaler les nids de poule sur les routes dans la ville de Gatineau.

    Le vrai pouvoir de l'application est dans la technologie IA que l'application utilise pour classifier les nids de poule assurer que les nids
    de poule les plus dangereux sont identifiés plus rapidement.

    **Selectionnez l'Interface Client pour soumettre une requête et l'Interface Employé voir où sont les nids de poule les plus prioritaires à Gatineau** 
    ### Qui sommes-nous?
    - Nom #1 : Description #1 [LinkedIn](https://www.linkedin.com/)
    - Nom #2 : Description #2 [LinkedIn](https://www.linkedin.com/)
    - Nom #3 : Description #3 [LinkedIn](https://www.linkedin.com/)
    - Nom #4 : Description #4 [LinkedIn](https://www.linkedin.com/)

    ### Methodes utilisées
    - YOLOv5
    - Folium
    - SQLite3
    - Streamlit
    - Geopy
    - Pgeocode
    - Nominatim
    - Pillow


    ### Remerciements
    Merci particulier à l'équipe du UHack 2024 pour l'organisation de cet événement et pour l'opportunité de travailler sur ce projet.
    Merci aux mentors pour leur soutien et leurs conseils tout au long de l'événement.
    Merci à tous les participants pour leur travail acharné et pour avoir mis la barre si haute.
    Merci aux sponsors pour leur soutien et leur générosité sans lesquels cet événement ne serait pas possible.

"""
)



