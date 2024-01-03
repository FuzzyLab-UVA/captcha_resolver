import os

from keras.models import load_model
from imutils import paths
import numpy as np
import cv2
import pickle

from spell_letters import adjust_kernel_size, is_near_edge
from etl_captcha import etl_images
from helpers import resize_to_fit



def captcha_resolver():
    with open("labels.dat", "rb") as f:
        lb = pickle.load(f)

    model = load_model('model_trained.hdf5')

    etl_images("./solve", "./solve")

    images = list(paths.list_images("./solve"))

    for image in images:
        print(f"Processando imagem: {image}")
        img = cv2.imread(image)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        img_thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        kernel_size = adjust_kernel_size(img.shape[:2])
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(img_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        img_height, img_width = img_morph.shape[:2]
        edge_margin = 10 

        letter_region = []

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if area > 100 or is_near_edge(x, y, w, h, img_width, img_height, edge_margin):
                letter_region.append((x, y, w, h))

        final_image = cv2.merge([img_morph] * 3)

        predict = list()

        for i, rectangle in enumerate(sorted(letter_region, key=lambda x: x[0])):
            print(f"Retângulo: {rectangle}")
            print(f"Índice: {i}")
            x, y, w, h = rectangle
            img_letter = img_morph[y:y+h+2, x:x+w+2]

            img_letter = resize_to_fit(img_letter, 20, 20)

            img_letter = np.expand_dims(img_letter, axis=2)
            img_letter = np.expand_dims(img_letter, axis=0)

            letters_predict = model.predict(img_letter)
            letters_predict = lb.inverse_transform(letters_predict)[0]
            predict.append(letters_predict)

    text_predict = "".join(predict)
    print(text_predict)
    return text_predict


if __name__ == "__main__":
    captcha_resolver()

    