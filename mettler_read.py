"""
Application to parse mettler toledo
balance output data.
"""

import re
import serial
import sys
from append_excel import ToCSV

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


def main():
    try:
        _filename = input("Input filename here - don't append .csv:\n")
        try:
            csv_file = ToCSV(_filename)
        except FileExistsError as e:
            print(e)
        scale_val = Scale()
        while True:
            byte_val = scale_val.get_value()
            str_val = scale_val.decode_to_str(byte_val)
            if not str_val:
                continue

            csv_file.write_csv(str_val)
            sys.stdout.write("  Weight: {}g   \r".format(str_val))
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nExiting application...")


if __name__ == '__main__':
    main()
