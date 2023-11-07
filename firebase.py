import time

import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from firebase_admin import db as rdb
import datetime
import cv2
import os
from . import settings as s  # this . avoids the module not found error

cwd = os.getcwd().replace('\\','/')
path = f"{cwd}/firebase/adminsdk_naveen.json"
cred = credentials.Certificate(path)

firebaseConfig = {
    "apiKey": "AIzaSyApnycwuuiVwoEL928RO7fodCTcEgNWesY",
    "authDomain": "smart-motion-detection.firebaseapp.com",
    "databaseURL": "https://smart-motion-detection-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "smart-motion-detection",
    "storageBucket": "smart-motion-detection.appspot.com",
    "messagingSenderId": "13665488472",
    "appId": "1:13665488472:web:83fcf3f86df24aa796842d",
    "measurementId": "G-WF45JXE642"
}
# Initialize firebase
app = firebase_admin.initialize_app(cred, firebaseConfig)
# getting firestore reference
db = firestore.client()
# reference for the firebase cloud storage
bucket = storage.bucket("smart-motion-detection.appspot.com")


def trigger_notification(payload: dict):
    # The topic name can be optionally prefixed with "/topics/".
    topic = 'smd'

    # See documentation on defining a message payload."
    name = payload.get("name")
    accuracy = payload.get("accuracy")
    message = messaging.Message(
        data={
            "message": f"Found {'Unknown Object Movement' if name.lower() == 'unknown' else name + ' with ' + str(accuracy) + ' % accuracy'}.",
            "image": payload.get("image"),
        },
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


def upload_image(mat_image, destination_path):
    _, buffer = cv2.imencode('.jpg', mat_image)
    image_bytes = buffer.tobytes()

    # Upload file to Cloud Storage
    blob = bucket.blob(destination_path)
    # blob.upload_from_filename(file_path)
    blob.upload_from_string(image_bytes, content_type='image/jpeg')

    # todo: change the signed url to public url.
    # Generate a signed URL for downloading the file
    download_url = blob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(days=7),  # Set the URL to expire in 15 minutes
        method='GET')

    # download_url = blob.public_url

    return download_url


def send_message(name, accuracy, image):
    doc_ref = db.collection('smd').document()

    # doc_ref.id this will give the id of the document.

    img_url = upload_image(image, f'smd/{doc_ref.id}')

    if img_url is not None:
        data = {
            'name': name,
            'accuracy': 0 if name.lower() == 'unknown' else accuracy,
            'image': img_url,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        # adding document to firestore.
        doc_ref.set(data)
        # triggering notification to devices with topic name "smd"
        trigger_notification(data)
        print("notification sent..")
    print(doc_ref.id)


def update_status(status: int):
    s.STATUS = status
    print(f"staus is {status}")
    rdb.reference("settings").update({"status": status})


def my_listener(event):
    # print(event.event_type)  # can be 'put' or 'patch'
    # print(event.path)  # relative to the reference, it seems
    # print(event.data)  # new data at /reference/event.path. None if deleted

    if event.path == "/":
        if len(event.data) == 1 and event.data.get("status") is not None:
            s.STATUS = event.data.get("status")
        else:
            s.ALARM_MODE = event.data.get("alarm_mode")
            # s.STATUS = event.data.get("status")
            update_status(1 if s.ALARM_MODE else 0)
            s.set_high_priority_time(event.data.get("high_priority_time"))
            s.set_low_priority_time(event.data.get("low_priority_time"))

    elif event.path == "/status":
        s.STATUS = event.data

    elif event.path == "/alarm_mode":
        s.ALARM_MODE = event.data
        # update_status(1 if s.ALARM_MODE else 0)

    elif event.path == "/high_priority_time":
        s.set_high_priority_time(event.data)

    elif event.path == "/low_priority_time":
        s.set_low_priority_time(event.data)


listener = rdb.reference('settings').listen(my_listener)

time.sleep(5)
update_status(-1)

def stop_listener():
    listener.close()

