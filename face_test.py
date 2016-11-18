from face_detect import *
from serial_client import *

client = SerialClient()
face = FaceDetection(client)

n = face.scan_for_faces()
print n
