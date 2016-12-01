#!/usr/bin/python
 
import spidev
import time

class SPIClient():

    def __init__(self):
        self.SPI = spidev.SpiDev()
        self.SPI.open(0, 0)
        self.max_speed_hz = 7629

    def write_state(self, state):
        bytes = [state+48] * 12
        bytes.append(10)
        for b in bytes:
            self.SPI.writebytes([b])

    def read_state(self):
        bytes = []

        while len(bytes) <= 12:
            byte = spi.readbytes(1)
            if(byte[0] != 0 and byte[0] != 10):
                bytes.append(byte[0])
            else:
                if(len(bytes) > 2):
                    break

        return "".join([chr(by) for by in bytes])