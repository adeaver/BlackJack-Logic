from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2, time
import serial.tools.list_ports, serial, time

def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "ttyACM" in p[0]:
            return p[0]
    return ""

def send_and_receive(ser, state):
    ser.write(state)
    inState = -1

    start_time = time.time()

    time.sleep(.01)

    while inState == -1:
        for c in ser.read():
            if(ord(c) != 13 and ord(c) != 10):
                try:
                    inState = int(c)
                    break
                except ValueError:
                    continue

            if(time.time() - start_time >= 2):
                ser.write(state)
                time.sleep(.01)
                start_time = time.time()


    return inState

port = find_arduino()
print port

ser = serial.Serial(port=port, baudrate=9600, timeout=.01)

ser.setRTS(True)
ser.setRTS(False)


state = 0
count_states = 0

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
camera = PiCamera()

camera.resolution = (640, 480)
camera.framerate = 30 

cap = PiRGBArray(camera, size=(640, 480))

box_width = 30

try:
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
              scan_state = send_and_receive(ser, "8")
              should_send = False

          cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
        cv2.rectangle(frame, (lower_bound, 0), (upper_bound, height), (0, 255, 0))

        if(should_send):
          scan_state = send_and_receive(ser, "7")

        #Display the resulting frame
        #cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

        cap.truncate(0)

        if scan_state == 9 or count_states >= 40:
            break
except KeyboardInterrupt:
    ser.close()

ser.close()

print "Done!"