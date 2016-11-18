import serial.tools.list_ports, serial, time, re

class SerialClient():

    def __init__(self):
        self.PORT = self.find_arduino()
        self.ser = None
        self.READ_TIMEOUT = 3 
        self.LAST_STATE_SENT = ""

        if(self.PORT != ""):
            self.ser = serial.Serial(port=self.PORT, baudrate=9600, timeout=1)
            print "Connected on port " + self.PORT

    def find_arduino(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "ttyACM" in p[0]:
                return p[0]
        return ""

    def connected(self):
        return self.ser is not None

    def send_and_receive(self, state):
        r_state = ""

        # clear the buffer
        self.get_input()
        
        while r_state == "":
            print "Sending state"
            self.send_state(state)
            r_state = self.get_input()

        return r_state
        

    def send_state(self, state):
        if(self.ser is not None):
            self.write(state)

    def receive_state(self):
        inp = ""

        while len(inp) < 1:
            inp = self.get_input()

            if(inp == "6666"):
                # corresponds to resend state
                self.send_current_state()
                inp = ""

        return inp

    def send_current_state(self):
        self.write(self.LAST_STATE_SENT)

    def write(self, msg):
        if(self.ser is not None):
            self.LAST_STATE_SENT = msg
            time.sleep(1)
            self.ser.setDTR(level=0)
            time.sleep(1)
            self.ser.write(msg)
            time.sleep(.05)

    def get_input(self):
        output = ""
        read = ""
        if(self.ser is not None):
            start_time = time.time()
            error_count = 3
            while True:
                try:
                    read = str(self.ser.readline())
                    output += read
                    if(read != ""):
                        break
                    else:
                        if(time.time() - start_time >= self.READ_TIMEOUT):
                            break
                except KeyboardInterrupt:
                    raise
                except:
                    if(error_count > 0):
                        start_time = time.time()
                        error_count -= 1
                    else:
                        break
        return re.sub("\n", "", output)

    def close_client(self):
        if(self.ser is not None):
            self.ser.close()
