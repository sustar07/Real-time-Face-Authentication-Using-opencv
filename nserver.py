import cv2
from deepface import DeepFace
import os

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

reference_dir = "C://Users//ajayu//Documents//Programming//Python//ML//Faceauth//"
reference_images = [os.path.join(reference_dir, filename) for filename in os.listdir(reference_dir) if filename.endswith('.jpg')]

def checkface(frame, image_paths):
    for image_path in image_paths:
        try:
            reference_image = cv2.imread(image_path)
            result = DeepFace.verify(frame, reference_image, enforce_detection=False)['verified']
            if result:
                print(f"Match found with reference image: {image_path}")
                return True  # Exit early if match is found
        except Exception as e:
            print(f"Error during face verification with {image_path}: {e}")
    
    return False  # No match found

def main():
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame from camera.")
            break

        # Perform face verification with all reference images
        match_found = checkface(frame, reference_images)

        # Display result based on match_found flag
        if match_found:
            cv2.putText(frame, "Match Found!!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Match Not Found!!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show the video frame
        cv2.imshow("Video", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release video capture and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()





