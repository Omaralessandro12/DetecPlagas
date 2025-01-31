import streamlit as st
from pathlib import Path
import PIL
import numpy as np
from PIL import Image
from skimage.transform import resize
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input
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
    
    preds = model.predict(x)[0]
    class_idx = np.argmax(preds)
    confidence = preds[class_idx]
    
    return class_idx, confidence

# Configuración del diseño de la página
st.set_page_config(
    page_title="Detección y Clasificación de Plagas en la Agricultura Mexicana",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Detección y Clasificación de Plagas en la Agricultura Mexicana")
st.write("Aplicación que ayuda a identificar las cinco plagas más comunes en la agricultura mexicana, como la araña roja, el pulgón verde, la mosca blanca, la mosca de la fruta y el picudo rojo.")

# Inicializar el estado para mostrar/ocultar la sección de ayuda
if 'show_help' not in st.session_state:
    st.session_state['show_help'] = False

# Mostrar u ocultar la sección de ayuda
def toggle_help():
    st.session_state['show_help'] = not st.session_state['show_help']

# Barra lateral
st.sidebar.header("Configuración del modelo de aprendizaje automático")

# Opciones de Modelos 
model_types_available = ['Yolov8', 'Resnet50']
selected_tasks = st.sidebar.multiselect("Seleccionar una Tarea", model_types_available, default=['Yolov8'])

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

# Imágenes predeterminadas
default_images = {
    "Araña Roja": "Imagenes/ar.jpg",
    "Mosca Blanca": "Imagenes/mb.jpg",
    "Mosca de la Fruta": "Imagenes/mf.jpg",
    "Picudo Rojo": "Imagenes/pr.jpg",
    "Pulgón Verde": "Imagenes/pv.jpg"
}

# Mostrar las imágenes predeterminadas en la barra lateral y permitir la selección
selected_image = st.sidebar.radio(
    "Selecciona una imagen predeterminada para cargar:",
    list(default_images.keys()),
    format_func=lambda x: f"{x}"
)

# Mostrar la imagen seleccionada en la barra lateral
st.sidebar.image(default_images[selected_image], caption=selected_image, use_column_width=True)

# Opción para que el usuario suba una imagen personalizada
fuente_img = st.sidebar.file_uploader("O sube una imagen desde su dispositivo...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

# Cargar la imagen seleccionada o la imagen subida por el usuario
if fuente_img:
    img = PIL.Image.open(fuente_img)
else:
    img = PIL.Image.open(default_images[selected_image])

# Mostrar la imagen seleccionada en la interfaz principal
st.image(img, caption=f"Imagen: {selected_image}", use_column_width=True)

# Botón para realizar la detección de plagas
if st.sidebar.button('Detectar Plaga'):
    col1, col2 = st.columns(2)

    with col1:
        try:
            st.image(img, caption="Imagen Original", use_column_width=True)
        except Exception as ex:
            st.error("Se produjo un error al abrir la imagen.")
            st.error(ex)

    with col2:
        if 'Yolov8' in models:
            res = models['Yolov8'].predict(img)
            boxes = res[0].boxes
            num_detections = len(boxes)
            res_plotted = res[0].plot()[:, :, ::-1]
            st.image(res_plotted, caption='Imagen Detectada por YOLOv8', use_column_width=True)
            st.write(f'Número de detecciones: {num_detections}')
            
            if 'Resnet50' in models and num_detections > 0:
                class_idx, confidence = model_prediction(np.array(img), models['Resnet50'])
                st.success(f'LA CLASIFICACION ES: {names[class_idx]} con una confianza del {confidence:.2%}')
                
        elif 'Resnet50' in models:
            class_idx, confidence = model_prediction(np.array(img), models['Resnet50'])
            st.image(img, caption='Imagen Detectada por Resnet50', use_column_width=True)
            st.success(f'LA CLASIFICACION ES  {names[class_idx]} con una confianza del {confidence:.2%}')

# Botón de ayuda justo debajo del botón de "Detectar Plaga"
st.sidebar.button('Ayuda', on_click=toggle_help)

# Mostrar la información de ayuda en la página principal si se ha activado
if st.session_state['show_help']:
    st.info("""
    **Nombre del Proyecto:** Detección y Clasificación de Plagas en la Agricultura Mexicana
    
    **Autor:** Omar Alejandro Ruiz Mendoza
    
    **Institución:** Universidad Autónoma Metropolitana - Unidad Azcapotzalco
    
    **Objetivos del Proyecto:**
    - Identificar las cinco plagas más comunes en la agricultura mexicana.
    - Proveer una herramienta que ayude a los agricultores a detectar plagas de manera temprana.
    
    **Justificación:**
    Este proyecto tiene como objetivo principal facilitar la detección temprana de plagas en cultivos agrícolas mediante el uso de tecnologías de aprendizaje automático. La identificación oportuna puede ayudar a reducir las pérdidas económicas y mejorar la productividad agrícola.
    """)
    if st.button('Cerrar'):
        st.session_state['show_help'] = False
