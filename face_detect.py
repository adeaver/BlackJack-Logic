import numpy as np
import cv2

class FaceDetection:

    def __init__(self, serial_client):
        self.face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
        self.cap = cv2.VideoCapture(0)
        self.serial_client = serial_client

    def scan_for_faces(self):
        scan_state = "0000"
        player_count = 0

        while "9" not in scan_state:
            should_send = True
            ret, frame = self.cap.read()

            height = frame.shape[0]
            width = frame.shape[1]

            lower_bound = (width/2)-5
            upper_bound = (width/2)+5

            faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
            for (x,y,w,h) in faces:
                if(x+w/2 >= lower_bound and x+w/2 <= upper_bound):
                    player_count += 1
                    scan_state = self.send_state("8888", player_count)
                    should_send = False

                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
            cv2.rectangle(frame, (lower_bound, 0), (upper_bound, height), (0, 255, 0))

            if(should_send):
                scan_state = self.send_state("7777", player_count)

             # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

        return player_count

    def send_state(self, state, player_count):
        #self.serial_client.send(state)
        #return self.serial_client.receive_state()
        if player_count == 5:
            return "9999"
        else:
            return "7777"

f = FaceDetection(None)
n = f.scan_for_faces()
print n