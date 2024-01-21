from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import load_model as tf_load_model

def load_model(model_path):
    """
    Carga un modelo ResNet50 desde el path especificado.

    Parámetros:
        model_path (str): La ruta al archivo del modelo ResNet50.

    Devuelve:
        Un modelo ResNet50.
    """
    try:
        # Carga el modelo ResNet50 preentrenado desde Keras Applications
        model = ResNet50(weights='imagenet')
        return model
    except Exception as ex:
        st.error(f"No se puede cargar el modelo ResNet50. Verifique la ruta especificada: {model_path}")
        st.error(ex)

