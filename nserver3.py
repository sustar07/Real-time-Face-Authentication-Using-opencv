import cv2
import csv

def register_new_face(camera_id, csv_file):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(camera_id)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame from camera.")
            break

        cv2.imshow('Register New Face - Press \'c\' to Capture, \'q\' to Quit', frame)

        key = cv2.waitKey(1)
        if key == ord('c'):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                cropped_face = frame[y:y+h, x:x+w]

                name = input("Enter the name for the new face: ")
                face_id = input("Enter a unique face ID (e.g., ABC001): ")

                with open(csv_file, 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([name, face_id])

                    face_filename = f"{face_id}.jpg"
                    cv2.imwrite(face_filename, cropped_face)

                print(f"Face ID '{face_id}' registered successfully for '{name}'.")
                
                # Display the registered user's name on the face box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.imshow('Registered Face', frame)
                cv2.waitKey(2000)  # Display the name for 2 seconds before continuing

                break

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage:
camera_id = 0
csv_file = 'registered_faces.csv'

# Register a new face using the camera
register_new_face(camera_id, csv_file)


def main():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow('Face Detection using Haar Cascades', frame)

        key = cv2.waitKey(1)
        if key == ord('r'):  # Press 'r' to register a new face
            register_new_face(0, 'registered_faces.csv')  # Use camera index 0 and specify CSV file path

        elif key == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
