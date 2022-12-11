# Face Authenticator With OTP
## Requirements (installable via pip)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [opencv-contrib-python](https://pypi.org/project/opencv-contrib-python/)
- [numpy](https://pypi.org/project/numpy/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [twilio](https://pypi.org/project/twilio/)

## What we used?
- [Twilio](https://www.twilio.com/) - for sending OTP - Twilio is a communications API for SMS, voice, video, WhatsApp messaging and email. We used this API to send and verfiy OTP by both as a web client and in the program itself.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - for verifing passcode - SpeechRecognition is a python library which we used to verfiy our passcode. The passcode is to be said by the user to proceed to the OTP verification Phase.
- [OpenCV](https://pypi.org/project/opencv-python/) - for face detection - OpenCV is a python library which we used to Detect the Face of the user using LBPH face recognition. Which is further compared to a Sample set of authorised Users we have in /FaceDetector 
- []
