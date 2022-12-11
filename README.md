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
- [OpenCV](https://pypi.org/project/opencv-python/) - for face detection - OpenCV is a python library which we used to Detect the Face of the user using LBPH face recognition. Then it is further compared to a Sample set of authorised Users we have in /FaceDetector 
- [Json](https://docs.python.org/3/library/json.html) - for labelling - Json is a python library which we used to label the Window for Face detection , Face identification and Sample Image set.

## How to run the program
1. **Download this GitHub repository**
	- Either Clone the repository
		```
		git clone https://github.com/Kunal-Attri/Lock-System.git
		```
	- Or download and extract the zip archive of the repository.

2. **Download & Install requirements**
	- Ensure that you have Python 3 installed.
	- Open terminal in the Repository folder on your local machine.
	- Run the following command to install requirements.
		```
		pip3 install -r requirements.txt
 		```

3. **Run CLI App `Sampling.py`**
      - Get Sample image Set of Authorised Users
               
	        python3 sampling.py
      - *Expected Interface*
            [the box with sampling]

4. **Run CLI App `main.py`**

       python3 main.py 
      - *Expected Interface*
           [the box of main.py]
5. **Preparing Data Set**
     - The collected data set from `Sampling.py` is further formatted for training in `FaceIdentificationModel.py`.
     - Here the Image gets loaded , formatted and grayscaled.
     - Then it gets passed on to `__build_dataset` where the mathematical Dataset is made.
     
6. **Training model on the data set collected from `Sampling.py`**
     - In `FaceIdentificationModel.py`, the function `__train_model` trains the Prepared Data set and gets the program ready for Face Detection using LBPH (Local Binary Pattern Histogram) Face Reecognition.

7. **Working**
     - **Face Detection**
        [ss of window with yellow square]
     - **Face Identification**
        [ss output of identified face]
     - **Passcode Verification**
        [ss output of voice verification]
     - **OTP Verifiction**
        [ss of recieved otp and verified otp]
     

