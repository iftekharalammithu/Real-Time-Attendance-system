import cv2
import face_recognition
import pickle
import os


## import images
imgs_folder = "img"
imgfacelist = []
img_name = []

for i in os.listdir(imgs_folder):
    full_path = os.path.join(imgs_folder, i)
    imgfacelist.append(cv2.imread(full_path))
    name = os.path.splitext(i)[0]
    img_name.append(name)


    print(len(imgfacelist))


def encode_img(imagelist):
    encode = []
    for img in imagelist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_en = face_recognition.face_encodings(img)[0]
        encode.append(face_en)

    return encode

allencodelist = encode_img(imgfacelist)

encodeliatwithname = [allencodelist,img_name]

file = open('encodefile.pkl', 'wb')

pickle.dump(encodeliatwithname,file)
file.close()