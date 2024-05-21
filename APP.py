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

# Seleccionado modelo, corregir para dos modelos a la vez
if selected_task == 'Yolov8':
    model_path = Path(ajustes.DETECCIÓN_MODEL)
elif selected_task == 'Resnet50':
    model_path = None  # Asignar None para omitir la carga del modelo

# Cargar modelo ML previamente entrenado
model_detection = None  # Inicializar el modelo de detección como None
model_classification = None  # Inicializar el modelo de clasificación como None

if model_path is not None:
    try:
        if 'Yolov8' in model_type:
            # Cargar el modelo YOLOv8 solo si está seleccionado
            model_detection = ayuda.load_model(model_path)
        if 'Resnet50' in model_type:
            # Cargar el modelo ResNet50 solo si está seleccionado
            model_classification = load_model(model_path)
    except Exception as ex:
        st.error(f"No se puede cargar el modelo. Verifique la ruta especificada: {model_path}")
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
                # Lógica para detectar utilizando YOLOv8
                res = model_detection.predict(uploaded_image)
                boxes = res[0].boxes
                num_detections = len(boxes)
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Imagen Detectada', use_column_width=True)
                # Mostrar el número de detecciones
                st.write(f'Número de detecciones: {num_detections}')

                # Clasificar la imagen detectada con Resnet50
                if num_detections > 0 and model_classification is not None and 'Resnet50' in model_type:
                    class_idx, confidence = model_prediction(np.array(uploaded_image), model_classification)
                    st.success(f'LA CLASE ES: {names[class_idx]} con una confianza del {confidence:.2%}')

            elif model_classification is not None and 'Resnet50' in model_type:
                # Lógica para clasificar solo con ResNet50
                res = model_classification.predict(uploaded_image)
                st.image(res, caption='Imagen Detectada por Resnet50', use_column_width=True)
                # Mostrar el número de detecciones
                num_detections = len(res)  # Calculamos el número de detecciones aquí
                st.write(f'Número de detecciones: {num_detections}')
