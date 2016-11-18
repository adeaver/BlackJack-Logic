from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2, time

class FaceDetection:

    def __init__(self, serial_client):
        self.face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
        self.camera = PiCamera()
        
        self.camera.resolution = (320, 240)
        self.camera.framerate = 30 

        self.cap = PiRGBArray(self.camera, size=(320, 240))

        self.serial_client = serial_client

        self.box_width = 10


    def scan_for_faces(self):
        scan_state = "0000"
        player_count = 0
        
        time.sleep(0.1)     

        for capture in self.camera.capture_continuous(self.cap, format="bgr", use_video_port=True):
            frame = capture.array
            should_send = True
            #ret, frame = self.cap.read()

            height = frame.shape[0]
            width = frame.shape[1]

            lower_bound = (width/2)-self.box_width
            upper_bound = (width/2)+self.box_width

            faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
            for (x,y,w,h) in faces:
                if(x+w/2 >= lower_bound and x+w/2 <= upper_bound):
                    player_count += 1
                    print "Detected new player"
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
 
            self.cap.truncate(0)
        # When everything done, release the capture
        #self.cap.release()
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
