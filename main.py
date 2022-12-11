import cv2
from datetime import datetime
from numpy import ndarray

from FaceDetectionModel import FaceDetectionModel
from FaceIdentificationModel import FaceIdentificationModel
from SpeechHandler import SpeechHandler
from TwilioHandler import TwilioHandler


MOBILE_NO = "+919605275844"
DATA_PATH = "FaceDetector/"
LABELS_PATH = "FaceDetector/labels.json"
MODEL_PATH = "model/trained_model.cv2"
PASSCODE = "lock"
VERIFIED_FLAG = False


def main() -> None:
    """
    Main method
    """
    runner = Main()
    while not VERIFIED_FLAG:
        runner.main()


class Main:
    def __init__(self) -> None:
        """
        Constructor: Initialization Script
        """
        self.__name = None
        self.__cap = cv2.VideoCapture(0)
        self.__face_detect = FaceDetectionModel()
        self.__face_identify = FaceIdentificationModel(data_path=DATA_PATH,
                                                       model_path=MODEL_PATH,
                                                       labels_path=LABELS_PATH)
        self.__speech = SpeechHandler()
        self.__verifier = TwilioHandler(mobile_no=MOBILE_NO)

    def main(self) -> None:
        """
        Main Script
        """
        ret, frame = self.__cap.read()
        if not ret:
            return

        image, face = self.__face_detect.detect(frame)
        if not len(face):
            return Main.frame_annotate(image, "Face not Found", color=(255, 0, 0))

        self.__name, identified = self.__face_identify.identify(face)
        if not identified:
            return Main.frame_annotate(image, "CANT RECOGNISE", color=(0, 0, 255))

        self.__handle_identified_face(image)
        if not self.__handle_speech_recognition():
            self.__verifier.send_message(f"Warning: {self.__name} tried to enter with Invalid Passphrase! "
                                         f"at {Main.__get_time()}")
            return
        if not self.__handle_otp_verification():
            self.__verifier.send_message(f"Warning: {self.__name} tried to enter with Invalid OTP! "
                                         f"at {Main.__get_time()}")
            return
        self.__handle_verified_user()

    def __handle_identified_face(self, img: ndarray) -> None:
        """
        Script for identified Face
        :param img: Annotated image with face
        """
        print(f"Hello {self.__name}")
        Main.frame_annotate(img, f"Hello {self.__name}", (0, 255, 0))

        time = Main.__get_time()
        self.__speech.speak("Face verified at " + time)

    def __handle_speech_recognition(self, sentence: str = None, try_flag: int = 1) \
            -> bool:
        """
        Script for Speech Recognition
        :param sentence: Initial sentence to be spoken
        """
        if sentence is None:
            sentence = f"Hello {self.__name}, speak your Passphrase!"
        self.__speech.speak(sentence)
        if PASSCODE in self.__speech.listen():
            print("Passphrase verified!")
            self.__speech.speak("Passphrase verified!")
            return True
        elif try_flag:
            return self.__handle_speech_recognition("Invalid Passphrase, try again.", try_flag - 1)
        print("Correct Passcode not provided within time!")
        self.__speech.speak("Correct passcode not provided within time!")
        return False

    def __handle_otp_verification(self) -> bool:
        """
        Script for OTP Verification
        """
        global VERIFIED_FLAG
        # if self.__verifier.auto_verify():
        #     VERIFIED_FLAG = True
        #     return True
        if self.__verifier.verify():
            VERIFIED_FLAG = True
            return True
        print("Correct OTP not entered within maximum tries!")
        self.__speech.speak("Correct OTP not entered within maximum tries!")
        return False

    def __handle_verified_user(self) -> None:
        print(f"{self.__name} verified!")
        self.__speech.speak(f"{self.__name} verified!")
        self.__verifier.send_message(f"Alert: {self.__name} successfully verified!")

    @staticmethod
    def frame_annotate(img: ndarray, text: str, color: tuple[int, int, int], position: tuple[int, int] = (250, 450)) \
            -> None:
        """
        Annotating a given video frame with text
        :param position: Position of annotation
        :param img: Frame image to be annotated
        :param text: Annotated text
        :param color: Color of annotated textx
        """
        cv2.putText(img, text, position, cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
        Main.__update_output_frame(img)

    @staticmethod
    def __update_output_frame(img: ndarray) -> None:
        """
        Updating the visible camera feed
        :param img: Updated frame image
        """
        cv2.imshow("Detector", img)
        cv2.waitKey(1)

    @staticmethod
    def __get_time():
        return datetime.now().strftime('%I:%M %p')

    def __del__(self) -> None:
        """
        Destructor: Closing Script
        """
        self.__cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
