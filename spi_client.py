#!/usr/bin/python
 
import spidev
import time

class SPIClient():

    def __init__(self):
        self.SPI = spidev.SpiDev()
        self.SPI.open(0, 0)
        self.max_speed_hz = 7629
        self.TIME_OUT = 4

    def write_state(self, state):
        bytes = [state+48] * 12
        bytes.append(10)
        for b in bytes:
            self.SPI.writebytes([b])

    def read_state(self):
        bytes = []

        print "Reading"

        start_time = time.time()
        valid_state = False
        next_state = -1

        while not valid_state:
            byte = self.SPI.readbytes(1)
            if(byte[0] != 0 and byte[0] != 10):
                bytes.append(byte[0])
            else:
                if(len(bytes) > 0):
                    valid_state, next_state = self.validate_state(bytes)

                    if(not valid_state):
                        bytes = []
                        self.write_state(6)

                        start_time = time.time()
                 elif(time.time() - start_time > self.TIME_OUT):
                    self.write_state(6)
                    start_time = time.time()
        #print next_state
        return next_state


    def validate_state(self, bytes):
        states = [0] * 10
        max_val = 0
        max_states = []

        for by in bytes:
            i = by - 48
            if i > 0 and i < 10:
                states[i] += 1

        for i in range(len(states)):
            if states[i] > max_val:
                max_val = states[i]
                max_states = [states[i]]
            elif states[i] == max_val:
                max_states.append(states[i])

        if len(max_states) > 1:
            return False, -1

        return True, max_states[0]
