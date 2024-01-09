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
    # page_icon="🤖",
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

# Seleccionado model, corregir para dos modelos a la vez
if selected_task == 'Yolov8':
    model_path = Path(ajustes.DETECCIÓN_MODEL)

# Cargar modelo ML previamente entrenado
try:
    model = ayuda.load_model(model_path)
except Exception as ex:
    st.error(f"No se puede cargar el modelo. Verifique la ruta especificada: {model_path}")
    st.error(ex)

# Cargar imagen directamente sin seleccionar fuente ni botón
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
        if st.sidebar.button('Detectar Plaga'):
            try:
                res = model.predict(uploaded_image)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Imagen Detectada', use_column_width=True)

                with st.expander("Detection Results"):
                    for box in boxes:
                        x_min, y_min, x_max, y_max, confianza, id_plaga = box.data
                        if id_plaga in info_plagas:
                            info = info_plagas[id_plaga]
                            st.write(f"Nombre: {info['nombre']}")
                            st.write(f"Plaga: {info['plaga']}")
                            st.write(f"Cómo combatir: {info['combate']}")
                        else:
                            st.write(f"Información no disponible para ID de plaga: {id_plaga}")

            except Exception as ex:
                st.error("Se produjo un error al realizar la detección.")
                st.error(ex)


                


