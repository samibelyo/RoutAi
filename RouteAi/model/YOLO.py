from ultralytics import YOLO
import streamlit as st
from PIL import Image
import torch


# Load your trained YOLO model
test_model = YOLO("best.pt", task="detect")

def preprocess_image(image, target_size=(640, 640)):
    if image.size == target_size:
        return image
    else:
        # Resize the image to the target size
        image = image.resize(target_size)
    return image

def make_prediction(img): 
    prediction = test_model(img,conf=0.2)
    prediction = prediction[0]                ## Dictionary with keys "boxes", "labels", "scores".
    return prediction


# Transformer les données (still in progress)
def transform_data_YOLO(df):
    transformed_df = df.copy()
    

    return transformed_df 




## Dashboard
st.title("detecteur nids de pouls")
upload = st.file_uploader(label="Upload Image :", type=["png", "jpg", "jpeg"]) ## Image as Bytes 


if upload:
    img1 = Image.open(upload)
    img=preprocess_image(img1)
    st.image(img)
    prediction = make_prediction(img)
    indice=prediction.boxes.conf

    st.header("indice de priorite")
    list_indice=[]
    
    for value in indice:
        list_indice.append(value.item()) 
    
    if len(list_indice) > 0:
        max_value = max(list_indice)
        st.write( max_value)
    else:
        st.write("Aucun nid de poule détecté.") 
        st.write(None)   
        

    
    
    
    
    





    
