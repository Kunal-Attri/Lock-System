import json
import os.path

import cv2
import uuid

from lib.FaceDetectionModel import FaceDetectionModel
from main import Main

NAME = "NoName"
SAMPLES = 150
DATA_PATH = "Dataset/"
LABELS_PATH = "Dataset/labels.json"


def main():
    global NAME, SAMPLES
    NAME = input("Name: ")
    face_detector = Sampler()
    while SAMPLES:
        if face_detector.main():
            SAMPLES -= 1


class Sampler(FaceDetectionModel):
    def __init__(self):
        super().__init__()
        self.__count = SAMPLES
        self.__cap = cv2.VideoCapture(0)
        self.__labels = dict()

    def write_json(self):
        if os.path.exists(LABELS_PATH):
            with open(LABELS_PATH, 'r') as file:
                file_data = json.load(file)
            self.__labels.update(file_data)
        with open(LABELS_PATH, "w") as file:
            json.dump(self.__labels, file, indent=4)

    def main(self):
        ret, frame = self.__cap.read()
        if not ret:
            return

        image, face = self.detect(frame)
        Main.frame_annotate(image, text=str(self.__count - SAMPLES), color=(200, 200, 200), position=(250, 450))

        if not self._face_count:
            return Main.frame_annotate(image, text="Face not Found", color=(0, 255, 0), position=(50, 50))
        elif self._face_count > 1:
            return Main.frame_annotate(image, text="Too many faces!", color=(255, 0, 0), position=(50, 50))

        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        uid = str(uuid.uuid4())
        file_name = DATA_PATH + uid + ".jpg"
        cv2.imwrite(file_name, face)
        self.__labels[uid] = NAME
        return 1

    def __del__(self):
        self.write_json()
        self.__cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
