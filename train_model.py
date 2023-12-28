import os
import pickle

from helpers import resize_to_fit

import cv2
import numpy as np
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

data = []
labels = []

dir_base_letters = 'base_letters'
images = paths.list_images(dir_base_letters)

for image_path in images:
    label = image_path.split(os.path.sep)[-2]
    if label[0] == '^':
        label = label[1:].upper()
    elif label == '__trash':
        label = 'trash'

    image = cv2.imread(image_path)
    if image is None or image.size == 0:
        print(f"Imagem inválida ou corrompida: {image_path}. Pulando.")
        continue  # Pula para a próxima imagem se esta for inválida

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    try:
        image = resize_to_fit(image, 20, 20)
    except cv2.error as e:
        print(f"Erro ao redimensionar a imagem {image_path}: {e}. Pulando.")
        continue  # Pula para a próxima imagem se houver um erro ao redimensionar

    image = np.expand_dims(image, axis=2)

    data.append(image)
    labels.append(label)

if len(data) != len(labels):
    raise ValueError("O número de imagens não corresponde ao número de rótulos!")

data = np.array(data, dtype='float') / 255
labels = np.array(labels)

(X_train, X_test, Y_train, Y_test) = train_test_split(data, labels, test_size=0.25, random_state=0)

lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# Determine o número de rótulos únicos
num_classes = len(lb.classes_)

with open('labels.dat', 'wb') as f:
    pickle.dump(lb, f)

model = Sequential()

model.add(Conv2D(20, (5, 5), padding='same', input_shape=(20, 20, 1), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(50, (5, 5), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Flatten())
model.add(Dense(500, activation='relu'))

# Adjust the final Dense layer to match the number of classes
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=26, epochs=10, verbose=1)

model.save('model_trained.hdf5')
