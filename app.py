"""
Application to parse mettler toledo
output weight and append current
date/time + weight to .csv file
specified by user.
"""

import os
import sys
from append_excel import ToCSV
from mettler_read import Scale
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    try:
        _filename = input("Input filename here - don't append .csv:\n")
        try:
            os.chdir(BASE_DIR+"/Data")
            csv_file = ToCSV(_filename)
        except (FileExistsError, FileNotFoundError) as e:
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
