import serial.tools.list_ports, serial, time

def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "ttyACM" in p[0]:
            return p[0]
    return ""

port = find_arduino()
print port

ser = serial.Serial(port=port, baudrate=9600, timeout=.01)
#ser.close()

#ser = serial.Serial(port=port, baudrate=9600)

ser.setRTS(True)
ser.setRTS(False)

try:
    while True:
        ser.write("7")
#        time.sleep(.2)
        for c in ser.read():
            if(ord(c) != 13 and ord(c) != 10):
                print c
        time.sleep(.01)
except KeyboardInterrupt:
    ser.close()
