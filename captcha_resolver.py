from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import cv2
import pickle
from etl_captcha import etl_images


def captcha_resolver():
    with open("labels.dat", "rb") as f:
        lb = pickle.load(f)

    model = load_model('model_trained.hdf5')

    etl_images("./solve", "./solve")