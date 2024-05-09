import cv2
import threading
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

reference = cv2.imread("ref1.jpg")

def checkface(frame):
    try:
        result = DeepFace.verify(frame, reference.copy())['verified']
        return result
    except Exception as e:
        print(f"Error in face verification: {e}")
        return False

while True:
    ret, frame = cap.read()

    if ret:
        if threading.active_count() < 5:  # Limit number of concurrent threads
            threading.Thread(target=checkface, args=(frame.copy(),)).start()

        match_result = checkface(frame)

        if match_result:
            cv2.putText(frame, "Match Found!!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "Match Not Found!!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
