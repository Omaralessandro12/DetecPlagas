from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input

import numpy as np
import streamlit as st
from PIL import Image
from skimage.transform import resize

# Path del modelo preentrenado
MODEL_PATH = 'modelo_resnet50.h5'

width_shape = 224
height_shape = 224

names = ['ARAÑA ROJA', 'MOSCA BLANCA', 'MOSCA FRUTA', 'PICUDO ROJO','PULGON VERDE']

def model_prediction(img, model):
    img_resize = resize(img, (width_shape, height_shape))
    x = preprocess_input(img_resize * 255)
    x = np.expand_dims(x, axis=0)
    
    preds = model.predict(x)[0]  # Solo obtenemos las predicciones para la primera imagen (índice 0)
    class_idx = np.argmax(preds)  # Índice de la clase predicha
    confidence = preds[class_idx]  # Nivel de confianza de la predicción
    
    return class_idx, confidence

def main():
    # Cargar el modelo
    model = load_model(MODEL_PATH)
    
    st.title("Clasificador de Aves :sunglasses:")

    predictS = ""
    img_file_buffer = st.file_uploader("Carga una imagen", type=["png", "jpg", "jpeg"])
    
    if img_file_buffer is not None:
        # Abrir la imagen y ajustar su tamaño
        image = Image.open(img_file_buffer)
        image_resized = image.resize((width_shape, height_shape))
        image_np = np.array(image_resized)
        
        st.image(image_resized, caption="Imagen", use_column_width=False)
    else:
        st.warning("No se ha seleccionado ninguna imagen.")

    if st.button("Predicción"):
        if img_file_buffer is not None:
            class_idx, confidence = model_prediction(image_np, model)
            st.success(f'LA CLASE ES: {names[class_idx]} con una confianza del {confidence:.2%}')
        else:
            st.warning("No se ha seleccionado ninguna imagen, por favor carga una imagen antes de realizar la predicción.")

if __name__ == '__main__':
    main()
