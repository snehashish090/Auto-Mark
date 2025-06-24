import face_recognition
import cv2
import numpy as np
from db import DataBase
import pyttsx3
import time 
engine = pyttsx3.init()
engine.setProperty('rate', 165) 

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names

db = DataBase()

# Running time of one class in seconds
auto_clear = 60*40

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

identified_faces = []

t1 = time.time()

while True:

    t2 = time.time()
    if (t2 - t1) > auto_clear:
        identified_faces = []
        t1 = t2
        continue
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) 
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:

            flag = False

            previous_faces = face_recognition.compare_faces(identified_faces, face_encoding)
            if True not in previous_faces:
                print("New Face Detected")
                print("Fetching faces from database")

                face_names = []

                people = db.get_people()
                known_face_encodings = people[1]
                known_face_names = people[0]
                flag = True

                identified_faces.append(face_encoding)

                print("Faces fetched")
            
            if known_face_encodings != []:
        
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                if flag and name!= "Unknown":
                    print(name, " was identified")
                    db.add_sighting(name)
                    engine.say(name+" was Identified")
                    engine.runAndWait()

                face_names.append(name)
            else:
                face_names.append("Unidentified")
            identified_faces.append(face_encoding)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

