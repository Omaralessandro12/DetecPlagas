# Paquetes integrados de Python
from pathlib import Path
import PIL

# Paquetes externos
import streamlit as st

# Módulos locales
import ajustes
import ayudaR  # Cambia este nombre según la estructura de tus archivos

# Configuracion del diseño de la página
st.set_page_config(
    page_title="Deteccion de Plagas en la agricultura Mexicana",
    # page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Detección de Plagas en la agricultura Mexicana")
st.write("APLICACIÓN PARA LA DETECCIÓN DE INSECTOS E ÁCAROS EN LA AGRICULTURA MEXICANA ")

# Barra lateral
st.sidebar.header("Configuración del modelo de aprendizaje automático")

# Opciones de Modelos
model_types_available = ['Yolov8', 'Resnet50']  # Agrega más tareas según sea necesario
model_type = st.sidebar.multiselect("Seleccionar tarea", model_types_available, default=['Yolov8', 'Resnet50'])

# Seleccionar modelo, corregir para dos modelos a la vez
yolov8_model_path = None
resnet50_model_path = None

if 'Yolov8' in model_type:
    yolov8_model_path = Path(ajustes.DETECCIÓN_MODEL)

if 'Resnet50' in model_type:
    RESNET_MODEL = st.sidebar.file_uploader("Selecciona el modelo ResNet50 (archivo HDF5):", type=("h5",))
    if RESNET_MODEL:
        st.sidebar.success("Modelo ResNet50 seleccionado correctamente.")
        resnet50_model_path = Path(RESNET_MODEL)

# Cargar modelos ML previamente entrenados
try:
    yolov8_model = ayudaR.load_model(yolov8_model_path)
except Exception as ex:
    st.error(f"No se puede cargar el modelo Yolov8. Verifique la ruta especificada: {yolov8_model_path}")
    st.error(ex)

try:
    resnet50_model = ayudaR.load_model(resnet50_model_path)
except Exception as ex:
    st.error(f"No se puede cargar el modelo ResNet50. Verifique la ruta especificada: {resnet50_model_path}")
    st.error(ex)

# Cargar imagen directamente
fuente_img = st.sidebar.file_uploader("Elige una imagen...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

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
        # Después de realizar la detección de plagas
        if st.sidebar.button('Detectar Plaga'):
            if 'Yolov8' in model_type:
                yolov8_res = yolov8_model.predict(uploaded_image)
                yolov8_boxes = yolov8_res[0].boxes
                num_yolov8_detections = len(yolov8_boxes)
                yolov8_res_plotted = yolov8_res[0].plot()[:, :, ::-1]
                st.image(yolov8_res_plotted, caption='Imagen Detectada por Yolov8', use_column_width=True)

            if 'Resnet50' in model_type:
                resnet50_res = resnet50_model.predict(uploaded_image)
                st.image(resnet50_res, caption='Imagen Detectada por Resnet50', use_column_width=True)

                # Mostrar el número de detecciones
                if 'Yolov8' in model_type:
                    st.write(f'Número de detecciones (Yolov8): {num_yolov8_detections}')


