import cv2
import threading

from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

counter = 0
facematch=False
reference= cv2.imread("ref.jpg")




def checkface(frame):
    global facematch
    try:
        if DeepFace.verify(frame, reference.copy())['verified']:
            facematch=True
        else:
            facematch=False

    except ValueError:
        pass

while True:
    ret , frame = cap.read()


    if ret:
        if counter %  30 ==0:
            try:
                threading.Thread(target=checkface, args=(frame.copy(),)).start()
            except ValueError:
                pass
            counter +=1

            if facematch:
                cv2.putText(frame,"Match Found!!", (20,450), cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
            
            else:
                cv2.putText(frame,"Match Not Found!!", (20,450), cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),3)
            cv2.imshow("video",frame)



    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    cv2.destroyAllWindows()
