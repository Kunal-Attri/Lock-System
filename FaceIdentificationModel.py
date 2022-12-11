from os import listdir
from os.path import isfile, join
from typing import Optional

import cv2
import numpy as np
from numpy import ndarray

# TODO: Loading a cv2 based saved model ... currently pass @Line27
# TODO: Save model via Pickle/Joblib


class FaceIdentificationModel:
    def __init__(self, data_path: Optional[str] = None, model_path: Optional[str] = None) -> None:
        """
        Constructor: Initialization Script
        :param data_path: Path to dataset
        :param model_path: Path to saved model pickle file
        """
        self.__model = None
        self.__data_path = data_path
        self.__model_path = model_path
        self.__image_files = list()
        self.__training_data = list()
        self.__labels = list()

        if self.__model_path is not None:
            pass
            # self.__import_trained_model()
        if self.__data_path is not None and self.__model is None:
            self.__generate_model()

    def identify(self, face: ndarray) -> bool:
        """
        Identify model w.r.t. trained model
        :param face: face image numpy array
        :return: Boolean
        """
        face = FaceIdentificationModel.image_to_grayscale(face)
        result = self.__model.predict(face)
        confidence = int(100 * (1 - (result[1]) / 300))
        if confidence > 85:
            return True
        return False

    def __import_trained_model(self) -> None:
        """
        Load a previously trained saved model
        """
        if isfile(self.__model_path):
            self.__model = cv2.face.LBPHFaceRecognizer()
            self.__model.load(self.__model_path)
            print("Model imported! Face detection is ready ...~_~...")

    def __export_trained_model(self) -> None:
        """
        Save a trained model
        """
        self.__model.save("model/trained_model.cv2")
        print("Trained Model is saved at model/trained_model.cv2")

    def __generate_model(self) -> None:
        """
        Script for generating model from dataset
        """
        self.__get_image_files()

        if self.__check_raw_dataset():
            self.__build_dataset()
        else:
            exit(1)

        self.__train_model()
        self.__export_trained_model()

    def __get_image_files(self) -> None:
        """
        Load Images from Dataset directory
        """
        print("Loading Image Dataset...")
        self.__image_files = [__f for __f in listdir(self.__data_path)
                              if (isfile(join(self.__data_path, __f))
                                  and (__f.endswith(".jpg") or __f.endswith(".png")))]

    def __check_raw_dataset(self) -> bool:
        """
        Conditional check for loaded raw dataset
        :return: Boolean
        """
        if len(self.__image_files) >= 50:
            return True
        else:
            if len(self.__image_files) == 0:
                print("Image Dataset is empty!")
            elif len(self.__image_files) <= 50:
                print("Image Dataset is too small!")
            print("Run sampling.py to sample your own image dataset!")
            return False

    def __build_dataset(self) -> None:
        """
        Building the mathematical dataset to train a model
        """
        print("Setting up the Dataset...")
        for __i, files in enumerate(self.__image_files):
            __image_path = self.__data_path + self.__image_files[__i]
            __image = FaceIdentificationModel.image_path_to_grayscale(__image_path)
            self.__training_data.append(np.asarray(__image, dtype=np.uint8))
            self.__labels.append(__i)
        self.__training_data = np.asarray(self.__training_data)
        self.__labels = np.asarray(self.__labels, dtype=np.int32)

    def __train_model(self) -> None:
        """
        Training Face Identification model
        """
        print("Getting Face Detection ready...")
        self.__model = cv2.face.LBPHFaceRecognizer_create()
        self.__model.train(self.__training_data, self.__labels)
        print("Face Detection is ready ...~_~...")

    @staticmethod
    def image_path_to_grayscale(image_path: str) -> ndarray:
        """
        Take image from location and convert it to grayscale
        :param image_path: Location of Image
        :return: Grayscale Image
        """
        image = cv2.imread(image_path)
        return FaceIdentificationModel.image_to_grayscale(image)

    @staticmethod
    def image_to_grayscale(image: ndarray) -> ndarray:
        """
        Convert an image into grayscale
        :param image: Image to be converted
        :return: Grayscale Image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

