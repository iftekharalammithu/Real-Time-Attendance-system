import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
from datetime import datetime


cred = credentials.Certificate("attendenceproject-ac782-firebase-adminsdk-b3dnu-f828c0e468.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://attendenceproject-ac782-default-rtdb.firebaseio.com/',
    'storageBucket' : 'attendenceproject-ac782.appspot.com'
    
    
})
bucket = storage.bucket()
## Video Show
videocam = cv2.VideoCapture(0)
videocam.set(3,640)
videocam.set(4,480)
backimg = cv2.imread('./Resources/background.png')

## import Modes
mode_folder = "Resources/Modes"
imgmodelist = []
for i in os.listdir(mode_folder):
    full_path = os.path.join(mode_folder, i)
    imgmodelist.append(cv2.imread(full_path))
    

##Load the encode file

file = open('encodefile.pkl', 'rb')

allencodelist , img_name = pickle.load(file)
file.close()

print(allencodelist)
print(img_name)

modetype = 0
counter = 0
ids = ''
img_ids = []

## Run Video
while True:
    rate , frame = videocam.read()

    imgs = cv2.resize(frame,(0,0), None, 0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_RGB2BGR)

    facecurrloc = face_recognition.face_locations(imgs)
    encodecurrimg = face_recognition.face_encodings(imgs,facecurrloc)


    backimg[162:162+480,55:55+640] = frame
    backimg[44 : 44+633 , 808 : 808+414] = imgmodelist[modetype]

    if facecurrloc:

        for enco , faceloc in zip(encodecurrimg, facecurrloc):
            matchs = face_recognition.compare_faces(allencodelist, enco)
            face_dis = face_recognition.face_distance(allencodelist, enco)
            matchindex = np.argmin(face_dis)

            if matchs[matchindex]:
                x1 , y1 ,x2 , y2 = faceloc
                y1, x2, y2, x1 = x1*4 , y1*4 ,x2*4 , y2*4
                # backimg = cv2.rectangle(backimg, (55 + x1, 162 + y1) , (x2 - x1, y2 - y1),(0, 0, 255), 2)
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                backimg = cvzone.cornerRect(backimg, bbox, rt=0)
                ids = img_name[matchindex]

                if counter == 0:
                    counter = 1
                    modetype = 1

        if counter != 0:
            if counter == 1:
                ## Get Data
                img_info = db.reference(f'stu/{ids}').get()
                print(img_info)
                

                ## Get img
                blob = bucket.get_blob(f'img/{ids}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                
                img_ids = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)

                datatimeobject = datetime.strptime(img_info['Last_attend'], "%Y-%m-%d %H:%M:%S")
                datetimedis = (datetime.now() - datatimeobject).total_seconds()
                print(datetimedis)

                if datetimedis > 300:

                    ## Update Attendence Database
                    ref = db.reference(f'stu/{ids}')
                    img_info["total_attend"] += 1

                    ref.child("total_attend").set(img_info["total_attend"])
                    ref.child("Last_attend").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modetype = 3
                    counter = 0
                    backimg[44 : 44+633 , 808 : 808+414] = imgmodelist[modetype]

            if modetype != 3:

                if 10 < counter < 20:
                    modetype = 2

                backimg[44 : 44+633 , 808 : 808+414] = imgmodelist[modetype]
                

                if counter <= 10:
                    ## Put Details in Frame
                    cv2.putText(backimg, str(img_info['total_attend']) , (861,125) , cv2.FONT_HERSHEY_COMPLEX , 2, (100,100,100) , 2)
                    (w , h) , _ = cv2.getTextSize(img_info['Name'] , cv2.FONT_HERSHEY_COMPLEX , 1 , 1)
                    off_side = (414 - w) // 2
                    cv2.putText(backimg, str(img_info['Name']) , (808+off_side,445) , cv2.FONT_HERSHEY_COMPLEX , 0.6, (50,50,50) , 1)
                    cv2.putText(backimg, str(img_info['com']) , (1006,550) , cv2.FONT_HERSHEY_COMPLEX , 0.6, (100,100,100) , 2)
                    cv2.putText(backimg, str(img_info['year']) , (1025,625) , cv2.FONT_HERSHEY_COMPLEX , 0.6, (100,100,100) , 2)
                    cv2.putText(backimg, str(ids) , (1006,493) , cv2.FONT_HERSHEY_COMPLEX , 0.6, (100,100,100) , 2)

                    backimg[175 : 175 + 216, 909 : 909 + 216] = img_ids

                counter += 1
                # print(counter)

                if counter >= 20:
                    counter = 0
                    modetype = 0
                    ids = ''
                    img_ids = []
                    backimg[44 : 44+633 , 808 : 808+414] = imgmodelist[modetype]


            
            # print(matchindex)
            # print(matchs)
            # print(face_dis)
    else:
        modetype = 0
        counter = 0

    # cv2.imshow('vid', frame)
    cv2.imshow('backimg', backimg)
    cv2.waitKey(1)