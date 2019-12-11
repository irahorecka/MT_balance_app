"""
Application to parse mettler toledo
balance output data.
"""

import time
import serial

class Scale:
    def __init__(self):
        self.ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 2400,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout=None
        )

    def get_value(self):
        byte_val = self.ser.readline()
        return byte_val

    def decode_to_str(self, _byte_val):
        num_list = []
        first_num = 0
        for i in _byte_val.decode('utf-8'):
            if first_num == 1:
                if i == '.':
                    num_list.append(i)
                    first_num = 0
                elif i == ' ':
                    first_num = 0
            if i.isdigit():
                num_list.append(i)
                first_num = 1
        
        return num_list


def main():
    scale_val = Scale()
    while True:
        byte_val = scale_val.get_value()
        str_val = byte_val.decode_to_str(byte_val)
        print(str_val)
