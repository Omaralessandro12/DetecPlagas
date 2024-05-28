import os    
import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

# Obtener la ruta al modelo dentro de la carpeta "weights"
model_path = os.path.join("weights", "nombre_del_modelo.h5")

# Cargar el modelo VGG16 preentrenado
model = tf.keras.models.load_model(model_path)

# Función para preprocesar la imagen
def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Función para realizar la predicción
def predict(image):
    preprocessed_img = preprocess_image(image)
    prediction = model.predict(preprocessed_img)
    return prediction

# Interfaz de usuario
st.title("Aplicación de Detección de Imágenes")

uploaded_image = st.file_uploader("Cargar una imagen")

if uploaded_image is not None:
    # Mostrar la imagen cargada
    image = Image.open(uploaded_image)
    st.image(image, caption='Imagen cargada', use_column_width=True)

    # Realizar la predicción cuando se presiona el botón
    if st.button('Detectar'):
        with st.spinner('Detectando...'):
            prediction = predict(image)
        st.success('Detección completada!')

        # Mostrar los resultados de la predicción
        st.write("Resultados de la predicción:")
        st.write(prediction)  # Aquí puedes ajustar cómo mostrar los resultados

