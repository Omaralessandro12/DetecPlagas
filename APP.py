# Paquetes integrados de Python
from pathlib import Path
import PIL
import numpy as np
from PIL import Image
from skimage.transform import resize

# Paquetes externos
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input

# Módulos locales
import ajustes
import ayudaR
import ayuda

# Configuración del diseño de la página
st.set_page_config(
    page_title="Deteccion de Plagas en la agricultura Mexicana",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path del modelo preentrenado
MODEL_PATH = 'modelo_resnet50.h5'
DETECTION_MODEL_PATH = ajustes.DETECCIÓN_MODEL

width_shape = 224
height_shape = 224

names = ['ARAÑA ROJA', 'MOSCA BLANCA', 'MOSCA FRUTA', 'PICUDO ROJO','PULGON VERDE']

def model_prediction(img, model, model_type):
    if model_type == 'Yolov8':
        # Implementa la lógica de detección de YOLOv8 aquí
        pass
    elif model_type == 'Resnet50':
        img_resize = resize(img, (width_shape, height_shape))
        x = preprocess_input(img_resize * 255)
        x = np.expand_dims(x, axis=0)
        
        preds = model.predict(x)[0]  # Solo obtenemos las predicciones para la primera imagen (índice 0)
        class_idx = np.argmax(preds)  # Índice de la clase predicha
        confidence = preds[class_idx]  # Nivel de confianza de la predicción
        
        return class_idx, confidence

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

# Seleccionado modelo, corregir para dos modelos a la vez
if selected_task == 'Yolov8':
    model_path = Path(DETECTION_MODEL_PATH)
elif selected_task == 'Resnet50':
    model_path = Path(MODEL_PATH)

# Cargar modelo ML previamente entrenado
model = None  # Inicializar el modelo como None
if model_path is not None:
    try:
        if selected_task == 'Yolov8':
            # Cargar el modelo YOLOv8
            model = ayuda.load_model(model_path)
        elif selected_task == 'Resnet50':
            # Cargar el modelo ResNet50
            model = load_model(model_path)
    except Exception as ex:
        st.error(f"No se puede cargar el modelo. Verifique la ruta especificada: {model_path}")
        st.error(ex)

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
            if model is not None:  # Solo ejecutar si se ha cargado un modelo
                if selected_task == 'Yolov8':
                    # Implementa la lógica de detección de YOLOv8 aquí
                    pass
                elif selected_task == 'Resnet50':
                    class_idx, confidence = model_prediction(np.array(uploaded_image), model, selected_task)
                    st.success(f'LA CLASE ES: {names[class_idx]} con una confianza del {confidence:.2%}')
