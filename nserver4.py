import cv2
import face_recognition
import numpy as np
import csv

known_face_encodings = []
known_face_names = []

def load_known_faces(csv_file):
    global known_face_encodings, known_face_names
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name, face_encoding_str = row
            face_encoding = np.array([float(num) for num in face_encoding_str.split()])
            known_face_names.append(name)
            known_face_encodings.append(face_encoding)

def save_known_faces(csv_file):
    global known_face_encodings, known_face_names
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for name, encoding in zip(known_face_names, known_face_encodings):
            encoding_str = ' '.join([str(num) for num in encoding])
            writer.writerow([name, encoding_str])

def register_new_face(frame, face_locations):
    if len(face_locations) != 1:
        print("Please ensure only one face is detected for registration.")
        return

    face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
    name = input("Enter the name for the new face: ")

    known_face_names.append(name)
    known_face_encodings.append(face_encoding)

def main(camera_id, csv_file):
    load_known_faces(csv_file)

    cap = cv2.VideoCapture(camera_id)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_locations = [(y, x+w, y+h, x)]
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow('Face Recognition', frame)

        key = cv2.waitKey(1)
        if key == ord('c'):  # Press 'c' to register a new face
            register_new_face(frame, faces)
            save_known_faces(csv_file)

        elif key == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_id = 0
    csv_file = 'known_faces.csv'

    main(camera_id, csv_file)
