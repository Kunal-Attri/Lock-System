import pyttsx3
import speech_recognition as sr
from speech_recognition import AudioData, UnknownValueError


class SpeechHandler:
    def __init__(self) -> None:
        """
        Constructor: Initialization Script
        """
        self.__engine = pyttsx3.init()
        self.__engine.setProperty('voice', self.__engine.getProperty('voices')[1].id)
        self.__engine.setProperty('rate', 130)
        self.__engine.setProperty('pitch', 200)

        self.__listener = sr.Recognizer()

    def speak(self, text: str) -> None:
        """
        Speaking the given text using Text-to-Speech
        :param text: Text to be spoken
        """
        self.__engine.say(text)
        self.__engine.runAndWait()

    def listen(self) -> str:
        """
        Listen to a voice and transcribe it into English sentences
        :return: Transcribed text
        """
        with sr.Microphone() as source:
            print("Listening...")
            voice = self.__listener.listen(source)
        return self.__transcribe(voice)

    def __transcribe(self, voice: AudioData) -> str:
        """
        Transcribe a given voice into English text
        :param voice: Given voice Input
        :return: Transcribed text
        """
        try:
            command = self.__listener.recognize_google(voice)
        except UnknownValueError:
            command = "-1"
        return command.lower() if command else self.listen()
