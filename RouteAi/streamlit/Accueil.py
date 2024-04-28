import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from streamlit_extras.let_it_rain import rain


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



# rain(
#         emoji="🐓",
#         font_size=54,
#         falling_speed=5,
#         animation_length="infinite",
#     )


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
for col, emoji, title, link in zip(row, ["👤", ":construction:"], ["Interface Citoyen", "Interface Employé"], ["http://localhost:8501/Citoyen", "http://localhost:8501/Employé"]):
    tile = col.container(height=170)
    tile.title(emoji)
    tile.link_button(title, link)


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Description",
                            "Qui sommes-nous?",
                            "Méthodes utilisées",
                            "Améliorations futures",
                            "Remerciements"])

tab1.markdown(
    """
    ### Description
    RoutAi est une application qui permet aux citoyens de signaler les nids de poule sur les routes dans la ville de Gatineau.

    Le vrai pouvoir de l'application est dans la technologie IA que l'application utilise pour classifier les nids de poule assurer que les nids
    de poule les plus dangereux sont identifiés plus rapidement.

    **Selectionnez l'Interface Client pour soumettre une requête et l'Interface Employé voir où sont les nids de poule les plus prioritaires à Gatineau** 
    """)

tab2.markdown(
    """
    ### Qui sommes-nous?
#### Adam Val Bonzil
Étudiant en Comptabilité et Gestion au Cégep Heritage College et Créateur et Propriétaire de AVB Solutions Agence de Marketing en Ligne [LinkedIn](https://www.linkedin.com/in/adam-val-bonzil-57022529b/)

#### Gabriel Lopez
Étudiant en Comptabilité et Gestion au Cégep Heritage College et Créateur et Président de Clear Legacy Inc. Compagnie de Commerce en Ligne [LinkedIn](https://www.linkedin.com/in/gabriel-lopez-510138256/)

#### Sami Belguesmia
Étudiant a l’UQO en maîtrise en intelligence artificielle et passionné de data science et Co-founder RoutAi [LinkedIn](https://www.linkedin.com/in/sami-belguesmia/)

#### Max Tixador
Étudiant au Baccalauréat en Administration des Affaires (concentration Finance) à l'UQO. Full-stack analyst pour PWHL Montréal (équipe de hockey féminin professionnelle) et freelancer full stack analyst spécialisé dans le sport professionel. Je crée des solutions et j'explique des données sportives depuis 4 ans. [LinkedIn](https://www.linkedin.com/in/max-tixador/)




    """)

tab3.markdown(
  """
  ### Methodes utilisées
    - [YOLOv8](https://github.com/ultralytics/yolov5) pour la détection de nids de poule
    - [Folium](https://python-visualization.github.io/folium/latest/) pour la visualisation des données
    - [SQLite3](https://www.sqlite.org/index.html) pour la gestion de la base de données
    - [Streamlit](https://streamlit.io) pour la création de l'interface utilisateur
    - [Geopy](https://geopy.readthedocs.io/en/stable/), [Pgeocode](https://pypi.org/project/pgeocode/) et [Nominatim](https://nominatim.org) pour la géolocalisation 
    - [Pillow](https://pillow.readthedocs.io/en/stable/) pour le traitement des images
    - [Pandas](https://pandas.pydata.org) pour la manipulation des données
    - [NumPy](https://numpy.org) pour le calcul scientifique 
    - [Docker](https://www.docker.com) pour la conteneurisation ### TODO
    - [Render](https://render.com) pour le déploiement 
    - [GitHub](https://github.com) et [Git](https://git-scm.com) pour le contrôle de version et le développement collaboratif
    - [ChatGPT-4](https://openai.com/chatgpt) pour la création du logo
    """)

tab4.markdown(
    """
    ### Améliorations futures
    - L’utilisation des méta-données dans une photo pour localiser les nids de poule sans adresse nécessaire
    - Création d’un trajet optimal selon les réparations prioritaires et la localisation actuelle du réparateur
    - Suivis qui permettent au citoyen de savoir si un nid de poule spécifique a déjà été signalé (pour éviter les double signalement) 
    """
)

tab5.markdown(
    """
    ### Remerciements
    - Merci particulier à l'équipe du UHack 2024 pour l'organisation de cet événement et pour l'opportunité de travailler sur ce projet.
    - Merci aux mentors pour leur soutien et leurs conseils tout au long de l'événement.
    - Merci à tous les participants pour leur travail acharné et pour avoir mis la barre si haute.
    - Merci aux sponsors pour leur soutien et leur générosité sans lesquels cet événement ne serait pas possible.
    """)


# st.markdown(
#     """
#     ### Description
#     RoutAi est une application qui permet aux citoyens de signaler les nids de poule sur les routes dans la ville de Gatineau.

#     Le vrai pouvoir de l'application est dans la technologie IA que l'application utilise pour classifier les nids de poule assurer que les nids
#     de poule les plus dangereux sont identifiés plus rapidement.

#     **Selectionnez l'Interface Client pour soumettre une requête et l'Interface Employé voir où sont les nids de poule les plus prioritaires à Gatineau** 
#     ### Qui sommes-nous?
#     - Nom #1 : Description #1 [LinkedIn](https://www.linkedin.com/)
#     - Nom #2 : Description #2 [LinkedIn](https://www.linkedin.com/)
#     - Nom #3 : Description #3 [LinkedIn](https://www.linkedin.com/)
#     - Nom #4 : Description #4 [LinkedIn](https://www.linkedin.com/)

#     ### Methodes utilisées
#     - [YOLOv5](https://github.com/ultralytics/yolov5) pour la détection de nids de poule
#     - [Folium](https://python-visualization.github.io/folium/latest/) pour la visualisation des données
#     - [SQLite3](https://www.sqlite.org/index.html) pour la gestion de la base de données
#     - [Streamlit](https://streamlit.io) pour la création de l'interface utilisateur
#     - [Geopy](https://geopy.readthedocs.io/en/stable/), [Pgeocode](https://pypi.org/project/pgeocode/) et [Nominatim](https://nominatim.org) pour la géolocalisation 
#     - [Pillow](https://pillow.readthedocs.io/en/stable/) pour le traitement des images
#     - [Pandas](https://pandas.pydata.org) pour la manipulation des données
#     - [NumPy](https://numpy.org) pour le calcul scientifique 
#     - [Docker](https://www.docker.com) pour la conteneurisation ### TODO
#     - [Render](https://render.com) pour le déploiement 
#     - [GitHub](https://github.com) et [Git](https://git-scm.com) pour le contrôle de version et le développement collaboratif


#     ### Remerciements
#     Merci particulier à l'équipe du UHack 2024 pour l'organisation de cet événement et pour l'opportunité de travailler sur ce projet.
#     Merci aux mentors pour leur soutien et leurs conseils tout au long de l'événement.
#     Merci à tous les participants pour leur travail acharné et pour avoir mis la barre si haute.
#     Merci aux sponsors pour leur soutien et leur générosité sans lesquels cet événement ne serait pas possible.

# """
# )


