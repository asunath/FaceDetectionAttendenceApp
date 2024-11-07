from celery import shared_task

import cv2
import face_recognition
from django.utils import timezone
from Facerecognition.models import Attendance
from User.models import userprofile
from datetime import datetime, timedelta



def mark_attendance(user):
    Attendance.objects.create(user=user.user, timestamp=timezone.now())



def load_known_face_encodings():
    known_users = []
    known_face_encodings = []

    profiles = userprofile.objects.all()
    for profile in profiles:
        known_users.append(profile)
        user_image = face_recognition.load_image_file(profile.image.path)
        encoded_image = face_recognition.face_encodings(user_image, num_jitters=5)  # Adjust num_jitters if needed
        known_face_encodings.append(encoded_image)

    return known_users, known_face_encodings



def process_frame(frame, known_face_encodings, known_users, users):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    if not face_locations:
        print("No face detected.")
        return

    got_image_facialfeatures = face_recognition.face_encodings(rgb_frame, num_jitters=5)
    if not got_image_facialfeatures:
        return

    user_names = []
    for got_image_encoding in got_image_facialfeatures:
        name = "Unknown"
        for index, existing_image_facialfeatures in enumerate(known_face_encodings):
            matches = face_recognition.compare_faces(existing_image_facialfeatures, got_image_encoding)
            if True in matches:
                user = known_users[index]
                name = user.name
                if user in known_users and user in users:
                    print(user.name)
                    mark_attendance(user)
                    users.remove(user)
        user_names.append(name)



@shared_task(bind=True)
def my_task(self):
    print("Running my task...")
    known_users, known_face_encodings = load_known_face_encodings()
    users = set(known_users)

    video_capture = cv2.VideoCapture(0)
    end_time = datetime.now() + timedelta(minutes=20)  # Run for 20 minutes
    
    while datetime.now() < end_time:
        ret, frame = video_capture.read()
        if not ret:
            break

        process_frame(frame, known_face_encodings, known_users, users)
    
    video_capture.release()
    print("Task completed and video capture released.")

