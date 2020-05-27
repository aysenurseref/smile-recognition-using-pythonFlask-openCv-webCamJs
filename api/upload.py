import cv2
import os
import numpy as np
from flask import Blueprint, request
from flask_json import json_response




uploadapi =  Blueprint('uploadapi', __name__, url_prefix='/api/v1/upload')
IMAGE_EXTENSIONS=[".png",".jpg","jpeg"]

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml') 
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml') 



def isImage(ext):
    return ext in IMAGE_EXTENSIONS



def is_smile(gray, frame): 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    result={}
    if faces is None:
        return  False
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w] 
        roi_color = frame[y:y + h, x:x + w] 
        smiles = smile_cascade.detectMultiScale(roi_gray,1.2) 
        print(smiles)
        if smiles is None:
            return False
        else:
            return True
    return False

@uploadapi.route("/snapshot",methods=["POST"])
def upload():
    try:
        obj = request.files.to_dict(flat=False)
        files = obj["snapshot"]
        file = files[0]
        print(file)
        name,ext = os.path.splitext(file.filename)
        if(isImage(ext)):
            filestr = file.read()
            npimg = np.fromstring(filestr, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            print(is_smile(gray, img))
            if is_smile(gray, img):
                return json_response(status_=200,success=True,result="Your form is sending..")
            else:
                return json_response(status_=200,success=False,result="Your form couldn't sent. you didn't smile :()")
    except Exception as e:
        return json_response(status_=200,success=False,result="An error occurred while uploading the file. "+str(e))
            

