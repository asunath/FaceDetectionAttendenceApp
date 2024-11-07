import cv2
import mediapipe as mp
import face_recognition

from django.shortcuts import render

from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor
from django.http import HttpResponse, StreamingHttpResponse

from User.models import userprofile
from Facerecognition.models import Attendance

# Create your views here.



# Global variable to track streaming status
streaming = False





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
        print("No face detected in the frame.")
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

    for (top, right, bottom, left), name in zip(face_locations, user_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        text_position = (left, top - 10)
        cv2.putText(frame, name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)



# Django view for starting the stream
def facerecognition(request):
    global streaming
    streaming = False
    if request.method == 'POST':
        form = request.POST.get('form_type')
        if form == 'stream':
            streaming = True

            def generate_frames():
                known_users, known_face_encodings = load_known_face_encodings()
                # copy of all known faces
                users = set(known_users)  # Convert to set for faster membership check

                recognized_users = []
                video_capture = cv2.VideoCapture(0)
                while True:
                    ret, frame = video_capture.read()
                    if not ret:
                        break

                    process_frame(frame, known_face_encodings, known_users, users)
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

    return render(request, "Admin/facerecognition.html")












































# def mark_attendance(user):
#     Attendance.objects.create(user=user, timestamp=timezone.now())

# def load_known_face_encodings():
#     known_users = []
#     known_face_encodings = []

#     profiles = userprofile.objects.all()
#     for profile in profiles:
#         known_users.append(profile)
#         user_image = face_recognition.load_image_file(profile.image.path)
#         encoded_image = face_recognition.face_encodings(user_image, num_jitters=5)
#         known_face_encodings.append(encoded_image)

#     return known_users, known_face_encodings

# def process_frame(frame, known_face_encodings, known_users, users):
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     face_locations = face_recognition.face_locations(rgb_frame)
#     if not face_locations:
#         print("No face detected in the frame.")
#         return

#     got_image_facialfeatures = face_recognition.face_encodings(rgb_frame, num_jitters=5)
#     if not got_image_facialfeatures:
#         return

#     def match_faces(got_image_encoding):
#         for index, existing_image_facialfeatures in enumerate(known_face_encodings):
#             matches = face_recognition.compare_faces(existing_image_facialfeatures, got_image_encoding)
#             if True in matches:
#                 user = known_users[index]
#                 if user in users:
#                     print(user.name)
#                     mark_attendance(user)
#                     users.remove(user)

#     with ThreadPoolExecutor() as executor:
#         executor.map(match_faces, got_image_facialfeatures)

#     for (top, right, bottom, left) in face_locations:
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#         text_position = (left, top - 10)
#         cv2.putText(frame, "Unknown", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# def generate_frames():
#     known_users, known_face_encodings = load_known_face_encodings()
#     users = set(known_users)

#     video_capture = cv2.VideoCapture(0)
#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             break

#         process_frame(frame, known_face_encodings, known_users, users)
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# def facerecognition(request):
#     if request.method == 'POST':
#         form = request.POST.get('form_type')
#         if form == 'stream':
#             while True:
#                 return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
#     return render(request, "Admin/facerecognition.html")
















# Django view for stopping the stream
def stop_stream(request):
    global streaming
    streaming = False
    return HttpResponse("Stream stopped")



def start_stream():
    # Object for drawing_utils
    mpDraw = mp.solutions.drawing_utils
    drawspec = mpDraw.DrawingSpec(thickness=1,circle_radius=1)
    # Object for face_mesh
    mpFaceMesh = mp.solutions.face_mesh
    # MediaPipe Face Mesh processes an RGB image and returns the face landmarks on each detected face
    # Object for FaceMesh class
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=3)

    # Captures each frames of the video
    # capture = cv2.VideoCapture('videos/sample1.mp4')
    capture = cv2.VideoCapture(0)

    while True :
        ret, frame = capture.read()
        if not ret :
            continue

        # Resize the frame
        resized = rescaleFrame(frame,scale=0.50)
        # Convert the frame to RGB
        RGB_frame = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
        # Processes an RGB image and returns the face landmarks on each detected face.
        result = faceMesh.process(RGB_frame)
        # Drawing landmarks
        if result.multi_face_landmarks:
            for landmarks in result.multi_face_landmarks:
                mpDraw.draw_landmarks(resized,landmarks,mpFaceMesh.FACEMESH_TESSELATION,drawspec,drawspec)

        # Display the frame
        cv2.imshow('Video',resized)
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        
    capture.release()
    cv2.destroyAllWindows()





# To rescale each frame
def rescaleFrame(frame,scale=0.75):
	#works on images,videos,live videos
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)
	dimensions = (width,height)
	return cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)



























# Inside IF condition
            # def stream_live():
            #     # Object for drawing_utils
            #     mpDraw = mp.solutions.drawing_utils
            #     drawspec = mpDraw.DrawingSpec(thickness=1,circle_radius=1)
            #     # Object for face_mesh
            #     mpFaceMesh = mp.solutions.face_mesh
            #     # MediaPipe Face Mesh processes an RGB image and returns the face landmarks on each detected face
            #     # Object for FaceMesh class
            #     faceMesh = mpFaceMesh.FaceMesh(max_num_faces=3)

            #     # Captures each frames of the video
            #     # capture = cv2.VideoCapture('videos/sample1.mp4')
            #     capture = cv2.VideoCapture(0)

            #     while True :
            #         ret, frame = capture.read()
            #         if not ret :
            #             continue

            #         # Resize the frame
            #         resized = rescaleFrame(frame,scale=0.50)
            #         # Convert the frame to RGB
            #         RGB_frame = cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
            #         # Processes an RGB image and returns the face landmarks on each detected face.
            #         result = faceMesh.process(RGB_frame)
            #         # Drawing landmarks
            #         if result.multi_face_landmarks:
            #             for landmarks in result.multi_face_landmarks:
            #                 mpDraw.draw_landmarks(resized,landmarks,mpFaceMesh.FACEMESH_TESSELATION,drawspec,drawspec)

            #         # Display the frame
            #         cv2.imshow('Video',resized)

            #         ret, buffer = cv2.imencode('.jpg', resized)
            #         frame_bytes = buffer.tobytes()
            #         yield (b'--frame\r\n'
            #             b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            # return StreamingHttpResponse(stream_live(), content_type='multipart/x-mixed-replace; boundary=frame')













# code copied from inside the form

            # global streaming
            # streaming = True
            # def generate_frames():
            #     known_users, known_face_encodings = load_known_face_encodings()

            #     # copy of all known faces
            #     users = set(known_users)  # Convert to set for faster membership check

            #     recognized_users = []

            #     with ThreadPoolExecutor() as executor:
            #         video_capture = cv2.VideoCapture(0)
            #         while True:  # Continue streaming until streaming is False
            #             ret, frame = video_capture.read()
            #             # cv2.imshow('Video', frame)
            #             if not ret:
            #                 continue

            #             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #             # Detect faces in the frame
            #             face_locations = face_recognition.face_locations(rgb_frame)
            #             if not face_locations:
            #                 print("No face detected in the frame.")
            #                 continue
            #             else:
            #                 # Encode the faces in the frame
            #                 got_image_facialfeatures = face_recognition.face_encodings(rgb_frame, num_jitters=5)  # Adjust num_jitters if needed

            #                 user_names = []
            #                 for got_image_encoding in got_image_facialfeatures:
            #                     futures = []
            #                     name = "Unknown"
            #                     for index, existing_image_facialfeatures in enumerate(known_face_encodings):
            #                         matches = face_recognition.compare_faces(existing_image_facialfeatures, got_image_encoding)
                                    
            #                         if True in matches:
            #                             user = known_users[index]
            #                             name = user.name

            #                             if user in known_users and user in users:
            #                                 print(user.name) # added
            #                                 futures.append(executor.submit(mark_attendance, user))
            #                                 users.remove(user)

            #                         user_names.append(name)

            #                     for future in futures:
            #                         future.result()  # Wait for completion


            #                 for (top, right, bottom, left), got_image_encoding in zip(face_locations, user_names):
            #                     # Draw a rectangle around the face
            #                     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)


            #                     # Calculate text position
            #                     text_position = (left, top - 10)
            #                     # Draw text
            #                     cv2.putText(frame, name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            #             # Encode frame to JPEG
            #             _, buffer = cv2.imencode('.jpg', frame)
            #             frame_bytes = buffer.tobytes()
            #             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            #             return StreamingHttpResponse(stream_live(), content_type='multipart/x-mixed-replace; boundary=frame')