from ultralytics import YOLO
import streamlit as st


import numpy as np
from PIL import Image
import av
import cv2

import ajustes


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model



