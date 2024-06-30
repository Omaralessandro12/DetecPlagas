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

# Define la función model_prediction
def model_prediction(img, model):
    width_shape = 224
    height_shape = 224

    img_resize = resize(img, (width_shape, height_shape))
    x = preprocess_input(img_resize * 255)
    x = np.expand_dims(x, axis=0)
    
    preds = model.predict(x)[0]  # Solo obtenemos las predicciones para la primera imagen (índice 0)
    class_idx = np.argmax(preds)  # Índice de la clase predicha
    confidence = preds[class_idx]  # Nivel de confianza de la predicción
    
    return class_idx, confidence

# Configuración del diseño de la página
st.set_page_config(
    page_title="Deteccion y clasificacion de Plagas en la agricultura Mexicana",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Detección de Plagas en la agricultura Mexicana")
st.write("APLICACIÓN PARA LA DETECCIÓN DE INSECTOS Y ÁCAROS EN LA AGRICULTURA MEXICANA")

# Barra lateral
st.sidebar.header("Configuración del modelo de aprendizaje automático")

# Opciones de Modelos 
model_types_available = ['Yolov8', 'Resnet50']  # Agrega más tareas según sea necesario
selected_tasks = st.sidebar.multiselect("Seleccionar tarea", model_types_available, default=['Yolov8'])

if not selected_tasks:
    st.error("Debes seleccionar al menos un modelo.")
    st.stop()

# Cargar modelos según la selección
models = {}
if 'Yolov8' in selected_tasks:
    yolov8_model_path = Path(ajustes.DETECCIÓN_MODEL)
    try:
        yolov8_model = ayuda.load_model(yolov8_model_path)
        models['Yolov8'] = yolov8_model
    except Exception as ex:
        st.error(f"No se puede cargar el modelo YOLOv8. Verifique la ruta especificada: {yolov8_model_path}")
        st.error(ex)

if 'Resnet50' in selected_tasks:
    resnet50_model_path = 'modelo_resnet50_3.h5'
    try:
        resnet50_model = load_model(resnet50_model_path)
        models['Resnet50'] = resnet50_model
    except Exception as ex:
        st.error(f"No se puede cargar el modelo ResNet50. Verifique la ruta especificada: {resnet50_model_path}")
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
            if 'Yolov8' in models:
                res = models['Yolov8'].predict(uploaded_image)
                boxes = res[0].boxes
                num_detections = len(boxes)
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Imagen Detectada por YOLOv8', use_column_width=True)
                st.write(f'Número de detecciones: {num_detections}')
                
                if 'Resnet50' in models and num_detections > 0:
                    class_idx, confidence = model_prediction(np.array(uploaded_image), models['Resnet50'])
                    st.success(f'LA CLASIFICACION ES: {names[class_idx]} con una confianza del {confidence:.2%}')
                    
            elif 'Resnet50' in models:
                class_idx, confidence = model_prediction(np.array(uploaded_image), models['Resnet50'])
                st.image(uploaded_image, caption='Imagen Detectada por Resnet50', use_column_width=True)
                st.success(f'LA CLASIFICACION ES  {names[class_idx]} con una confianza del {confidence:.2%}')
