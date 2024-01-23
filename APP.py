# Paquetes integrados de Python
from pathlib import Path
import PIL

# Paquetes externos
import streamlit as st

# Módulos locales
import ajustes
import ayuda

# Configuracion del diseño de la página

st.set_page_config(
    page_title="Deteccion de Plagas en la agricultura Mexicana",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Detección de Plagas en la agricultura Mexicana")
st.write("APLICACIÓN PARA LA DETECCIÓN DE INSECTOS E ACAROS EN LA AGRICULTURA MEXICANA ")

# Barra lateral
st.sidebar.header("Configuración del modelo de aprendizaje automático")

# Opciones de Modelos 
model_types_available = ['Yolov8', 'Resnet50']  # Agrega más tareas según sea necesario
model_type = st.sidebar.multiselect("Seleccionar tarea", model_types_available, default=['Yolov8'])

if not model_type:
    model_type = ['Yolov8']

selected_task = model_type[0]

# Seleccionado modelo, corregir para dos modelos a la vez
if selected_task == 'Yolov8':
    model_path = Path(ajustes.DETECCIÓN_MODEL)
elif selected_task == 'Resnet50':
    model_path = Path(ajustes.RESNET_MODEL)

# Cargar modelo ML previamente entrenado
try:
    model = ayuda.load_model(model_path)
except Exception as ex:
    st.error(f"No se puede cargar el modelo. Verifique la ruta especificada: {model_path}")
    st.error(ex)

# Cargar imagen directamente  
fuente_img = st.sidebar.file_uploader("Elige una imagen...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

# Variable para controlar si mostrar solo la detección
show_detection_only = False

if fuente_img:
    col1, col2 = st.columns(2)

    with col1:
        try:
            if fuente_img:
                uploaded_image = PIL.Image.open(fuente_img)
                st.image(fuente_img, caption="Imagen Cargada", use_column_width=True)
        except Exception as ex:
            st.error("Se produjo un error al abrir la imagen.")
            st.error(ex)

    with col2:        
        if st.sidebar.button('Detectar Plaga'):
            show_detection_only = True
            if selected_task == 'Yolov8':
                res = model.predict(uploaded_image)
                boxes = res[0].boxes
                num_detections = len(boxes)
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Imagen Detectada', use_column_width=True)
            elif selected_task == 'Resnet50':
                # llamada a resnet50
                res = model.predict(uploaded_image)
                # visualizacion resnet 
                st.image(res, caption='Imagen Detectada por Resnet50', use_column_width=True)
             # Mostrar el número de detecciones
            st.write(f'Número de detecciones: {num_detections}')

# Mostrar solo la detección si show_detection_only es True
if show_detection_only and selected_task == 'Yolov8':
    st.image(res_plotted, caption='Imagen Detectada', use_column_width=True)
elif show_detection_only and selected_task == 'Resnet50':
    st.image(res, caption='Imagen Detectada por Resnet50', use_column_width=True)
