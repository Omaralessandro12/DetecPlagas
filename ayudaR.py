from torchvision.models import resnet50
import torch

def load_model(model_path):
    """
    Loads a ResNet50 model from the specified model_path.

    Parameters:
        model_path (str): The path to the ResNet50 model file.

    Returns:
        A ResNet50 model.
    """
    # Cargar el modelo pre-entrenado
    model = resnet50(pretrained=False)
    # Cargar los pesos pre-entrenados del archivo
    model.load_state_dict(torch.load(model_path))
    # Establecer el modo de evaluación
    model.eval()
    return model

