from face_detect import *
from spi_client import *

client = SPIClient()
face = FaceDetection(client)

n = face.scan_for_faces()
print n
