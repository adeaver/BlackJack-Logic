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
        #print bytes
        bytes.append(10)
        for b in bytes:
            self.SPI.writebytes([b])

    def read_state(self):
        bytes = []

        start_time = time.time()

        while len(bytes) < 12:
            byte = self.SPI.readbytes(1)
            if(byte[0] != 0 and byte[0] != 10):
                bytes.append(byte[0])
		print byte[0]
            else:
                if(len(bytes) > 5):
                    break
            if(time.time() - start_time >= self.TIME_OUT):
                bytes = []
                self.write_state(6)
                start_time = time.time()

        states = [0] * 9

        for by in bytes:
            states[by-48] += 1

        max_state = 0
        max_val = 0
        for i in range(len(states)):
            if(states[i] > max_val):
                 max_state = i
                 max_val = states[i]

	print max_state
        return max_state
