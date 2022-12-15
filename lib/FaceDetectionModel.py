import cv2
import numpy as np
from numpy import ndarray

from lib.FaceIdentificationModel import FaceIdentificationModel


class FaceDetectionModel:
    def __init__(self) -> None:
        """
        Constructor: Initialization Script
        """
        self.__face_classifier = None
        self._face_count = 0
        self.__set_face_classifier()

    def detect(self, frame: ndarray) -> tuple[ndarray, ndarray]:
        """
        Detect faces in a frame and return them
        :param frame: Image
        :return: Annotates frame, face positions
        """
        image = FaceIdentificationModel.image_to_grayscale(frame)
        faces = self.__face_classifier.detectMultiScale(image, 1.3, 5)
        self._face_count = len(faces)
        return FaceDetectionModel.__annotate_faces(frame, faces)

    def __set_face_classifier(self) -> None:
        """
        To set Face Classifier
        """
        self.__face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    @staticmethod
    def __annotate_faces(frame: ndarray, faces: tuple[ndarray, ...]) -> tuple[ndarray, ndarray]:
        """
        Annotate faces on the frame
        :param frame: Image
        :param faces: Face Positions
        :return: Annotated frame, Face positions
        """
        roi = np.ndarray((0, 0, 0))
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi = frame[y:y + h, x:x + w]
            roi = cv2.resize(roi, (200, 200))
        return frame, roi
