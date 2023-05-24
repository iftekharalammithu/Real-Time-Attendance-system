import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("attendenceproject-ac782-firebase-adminsdk-b3dnu-f828c0e468.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://attendenceproject-ac782-default-rtdb.firebaseio.com/'
    
    
})

ref = db.reference('stu')

data = {
    "elon": {
        "Name" : 'elon',
        "com" : 'spacex',
        "year" : 2014,
        "total_attend" : 6,
        "Last_attend" : "2023-05-23 15:35:30"
    } ,

    "emili": {
        "Name" : 'Emili',
        "com" : 'Actor',
        "year" : 2014,
        "total_attend" : 6,
        "Last_attend" : "2023-05-23 15:40:30"
    } ,

    "jeff": {
        "Name" : 'Jeff',
        "com" : 'Amazon',
        "year" : 2014,
        "total_attend" : 6,
        "Last_attend" : "2023-05-23 16:35:30"
    } ,

    "mithu": {
        "Name" : 'Mithu',
        "com" : 'Programmer ',
        "year" : 2014,
        "total_attend" : 6,
        "Last_attend" : "2023-05-23 17:35:30"
    }
}

for key , value in data.items():
    ref.child(key).set(value)
