"""
Parse mettler toledo balance output
data.
"""

import re
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
        decoded_bytes = _byte_val.decode('utf-8')
        num_val_list = re.findall(r"[-+]?\d*\.\d+|\d+", decoded_bytes)
        try:
            num_val = num_val_list[0]
        except IndexError:
            num_val = None
        return num_val    
