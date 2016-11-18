from serial_client import *

client = SerialClient()

#print client.send_and_receive("2222")

client.send_state("2222")
print client.receive_state()
