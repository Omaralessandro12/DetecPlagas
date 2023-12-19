from pathlib import Path
import sys

# Obtiene la ruta absoluta del archivo actual
file_path = Path(__file__).resolve()

# Obtiene el directorio principal del archivo actual
root_path = file_path.parent

# Agregar la ruta raíz a la lista sys.path si aún no está allí
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Obtener la ruta relativa del directorio raíz con respecto al directorio de trabajo actual
ROOT = root_path.relative_to(Path.cwd())

# Fuentes
IMAGE = 'Imagen'


LISTA_FUENTES = [IMAGE ]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'office_4.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'office_4_detected.jpg'


# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECCIÓN_MODEL = MODEL_DIR / 'best.pt'
SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'

# Webcam
WEBCAM_PATH = 0
