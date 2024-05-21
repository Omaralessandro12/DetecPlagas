from pathlib import Path
import PIL
import numpy as np
from PIL import Image
from skimage.transform import resize

# Paquetes externos
import streamlit as st
import torch
import tensorflow as tf

# Define la función model_prediction para PyTorch
def model_prediction_pytorch(img, model):
    # Preprocesamiento de la imagen
    img = np.array(img.resize((224, 224)))  # Redimensionar la imagen a 224x224
    img = img.transpose((2, 0, 1))  # Cambiar el formato de los canales (H, W, C) a (C, H, W)
    img = img / 255.0  # Normalizar los valores de píxeles al rango [0, 1]
    img = torch.FloatTensor(img).unsqueeze(0)  # Convertir a tensor y agregar una dimensión adicional (batch)
    
    # Realizar la predicción
    with torch.no_grad():
        output = model(img)
        _, predicted = torch.max(output, 1)
    
    return predicted.item()

# Configuración del diseño de la página
st.set_page_config(
    page_title="Deteccion de Plagas en la agricultura Mexicana",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Detección de Plagas en la agricultura Mexicana")
st.write("APLICACIÓN PARA LA DETECCIÓN DE INSECTOS Y ÁCAROS EN LA AGRICULTURA MEXICANA")

# Barra lateral
st.sidebar.header("Configuración del modelo de aprendizaje automático")

# Opciones de Modelos 
model_types_available = ['Yolov8', 'Resnet50']  # Agrega más tareas según sea necesario
model_type = st.sidebar.multiselect("Seleccionar tarea", model_types_available, default=['Yolov8'])

if not model_type:
    st.error("Debes seleccionar al menos un modelo.")
    st.stop()

# Seleccionado modelo
selected_task = model_type[0]

# Cargar modelo ML previamente entrenado
model_detection = None  # Inicializar el modelo de detección como None
model_classification = None  # Inicializar el modelo de clasificación como None

if 'Yolov8' in model_type:
    try:
        if selected_task == 'Yolov8':
            # Cargar el modelo YOLOv8 (no incluido en este ejemplo, asegúrate de tener la función para cargarlo)
            model_detection = load_yolov8_model()
    except Exception as ex:
        st.error(f"No se puede cargar el modelo YOLOv8. Verifique la ruta especificada.")
        st.error(ex)

if 'Resnet50' in model_type:
    try:
        if selected_task == 'Resnet50':
            # Cargar el modelo ResNet50 en formato h5 (este es un ejemplo, debes proporcionar la ruta correcta)
            model_classification = tf.keras.models.load_model('modelo_resnet50.h5')
    except Exception as ex:
        st.error(f"No se puede cargar el modelo ResNet50. Verifique la ruta especificada.")
        st.error(ex)

names = ['ARAÑA ROJA', 'MOSCA BLANCA', 'MOSCA FRUTA', 'PICUDO ROJO','PULGON VERDE']

# Cargar imagen directamente  
fuente_img = st.sidebar.file_uploader("Elige una imagen...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

if fuente_img:
    if st.sidebar.button('Detectar Plaga'):
        col1, col2 = st.columns(2)

        with col1:
            try:
                if fuente_img:
                    uploaded_image = PIL.Image.open(fuente_img)
                    st.image(uploaded_image, caption="Imagen Original", use_column_width=True)
            except Exception as ex:
                st.error("Se produjo un error al abrir la imagen.")
                st.error(ex)

        with col2:        
            if model_detection is not None and 'Yolov8' in model_type:
                # Lógica para detectar utilizando YOLOv8 (debes implementar la función para cargar el modelo YOLOv8)
                # res = model_detection.predict(uploaded_image)
                # Implementa la lógica para la detección con YOLOv8 aquí
                st.error("Lógica de detección YOLOv8 no implementada aún.")
                
                # Clasificar la imagen detectada con Resnet50
                if model_classification is not None and 'Resnet50' in model_type:
                    class_idx = model_prediction_pytorch(uploaded_image, model_classification)
                    st.success(f'LA CLASE ES: {names[class_idx]}')

            elif model_classification is not None and 'Resnet50' in model_type:
                # Lógica para clasificar solo con ResNet50
                # Implementa la lógica para la clasificación con ResNet50 aquí
                st.error("Lógica de clasificación ResNet50 no implementada aún.")
