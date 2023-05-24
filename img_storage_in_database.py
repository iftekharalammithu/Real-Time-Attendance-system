import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os


cred = credentials.Certificate("attendenceproject-ac782-firebase-adminsdk-b3dnu-f828c0e468.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://attendenceproject-ac782-default-rtdb.firebaseio.com/',
    'storageBucket' : 'attendenceproject-ac782.appspot.com'
    
    
})

imgs_folder = "img"

for i in os.listdir(imgs_folder):
    
    full_path = f'{imgs_folder}/{i}'

    bucket = storage.bucket()
    blob = bucket.blob(full_path)
    blob.upload_from_filename(full_path)


