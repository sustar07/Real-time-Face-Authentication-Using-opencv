import cv2
import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["faceauth"]
collection = db["users"]

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_roi = frame[y:y + h, x:x + w]

        if cv2.waitKey(1) & 0xFF == ord('c'):
            user_id = input("Enter ID: ")
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            phone = input("Enter Phone Number: ")
            position = input("Enter Position: ")

            user_data = {
                "id": user_id,
                "name": name,
                "email": email,
                "phone": phone,
                "position": position
            }

            # Save face image with user ID as file name
            save_path = f"{user_id}.jpg"
            cv2.imwrite(save_path, face_roi)
            print(f"Face image saved as {save_path}")

            # Insert user data into MongoDB
            collection.insert_one(user_data)
            print("User data inserted into MongoDB")

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
