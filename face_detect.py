from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2, spidev, time

def send_and_receive(spi, state):
    spi.writebytes([state])

    while True:
        b = spi.readbytes(1)
        if(b[0] != 0):
            print "RECEIVED " + str(b[0])
            return b[0]

    return -1

spi = spidev.SpiDev()
spi.open(0, 1)
state = 0
count_states = 0

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
camera = PiCamera()

camera.resolution = (640, 480)
camera.framerate = 30 

cap = PiRGBArray(camera, size=(640, 480))

box_width = 30

for capture in camera.capture_continuous(cap, format="bgr", use_video_port=True):
    count_states += 1
    print "Capturing..."
    frame = capture.array
    should_send = True
    #ret, frame = cap.read()

    height = frame.shape[0]
    width = frame.shape[1]

    lower_bound = (width/2)-box_width
    upper_bound = (width/2)+box_width

    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
    for (x,y,w,h) in faces:
      if(x+w/2 >= lower_bound and x+w/2 <= upper_bound):
          print "Detected new player"
          scan_state = send_and_receive(spi, 8)
          should_send = False

      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
    cv2.rectangle(frame, (lower_bound, 0), (upper_bound, height), (0, 255, 0))

    if(should_send):
      scan_state = send_and_receive(spi, 9)

    #Display the resulting frame
    #cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

    cap.truncate(0)

    if scan_state == 9 or count_states >= 40:
        break

print "Done!"