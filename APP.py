# Paquetes integrados de Python
from pathlib import Path
import PIL

# Paquetes externos
import streamlit as st

# Módulos locales
import ajustes
import ayudaR
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
model_types_available = ['Resnet50']  # Solo se permite Resnet50
model_type = st.sidebar.multiselect("Seleccionar tarea", model_types_available, default=['Resnet50'])

if not model_type:
    st.error("Debes seleccionar al menos un modelo.")
    st.stop()

selected_task = model_type[0]

# Seleccionado modelo
model_path = None  # Asignar None para omitir la carga del modelo

# Cargar modelo ML previamente entrenado
model = None  # Inicializar el modelo como None
if model_path is not None:
    try:
        model = ayudaR.load_model(model_path)
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
                if selected_task == 'Resnet50':
                    # llamada a resnet50
                    res = model.predict(uploaded_image)
                    # visualizacion resnet 
                    st.image(res, caption='Imagen Detectada por Resnet50', use_column_width=True)
                    # Mostrar el número de detecciones
                    num_detections = len(res)  # Calculamos el número de detecciones aquí
                    st.write(f'Número de detecciones: {num_detections}')
