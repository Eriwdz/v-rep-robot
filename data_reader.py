import os
import pickle
import random

import cv2
import dlib
import numpy as np
from imutils import resize


class DataReader:
    detector = dlib.get_frontal_face_detector()

    @staticmethod
    def read(root_path: str):
        X, y = DataReader.read_gender(f"{root_path}/male", "male")
        X1, y1 = DataReader.read_gender(f"{root_path}/female", "female")
        X, y = X[:len(X1)], y[:len(y1)]
        X.extend(X1), y.extend(y1)
        col = X[0].shape[0]
        combined = list(zip(X, y))
        random.shuffle(combined)
        X[:], y[:] = zip(*combined)
        return np.asarray(X).reshape(-1, col), np.asarray(y).reshape(-1)

    @staticmethod
    def read_gender(path, gender):
        X, y = [], []
        gender = int(gender == "male")
        for file in os.listdir(path):
            with open(f"{path}/{file}", "rb") as f:
                temp = pickle.load(f, encoding="latin1")
                X.append(temp)
                y.append(gender)
        return X, y

    @staticmethod
    def read_image(image_path: str):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        rects = DataReader.detector(image, 2)
        rect = rects[0]
        image = image[rect.top():rect.bottom(), rect.left():rect.right()]
        image = resize(image, 30, 30)
        cv2.imwrite("test.jpg", image)
        image = image.reshape(1, -1)
        return image
