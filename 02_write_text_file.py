import os
import sys
import argparse
import time
import re


def normalize_filename(filename):
    return re.sub(r'[\\\/\.\#\%\$\!\@\(\)\[\]\s]+', '_', filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Inject a text file to Windows Desktop.')
    parser.add_argument('-f', type=str, default=os.path.basename(__file__), help='input file')
    #parser.add_argument('-f', type=str, required=True, help='input file')

    args = parser.parse_args()

    print('input_file:', args.f)
    print(os.path.exists(args.f))
    if args.f is not None and os.path.exists(args.f):
        basename = os.path.basename(args.f)
        # create duck script
        duck_filename = normalize_filename(args.f) + '.duck'

        print(duck_filename)
        with open(args.f, mode='r') as text_file, open(duck_filename, mode='w') as duck_file:
            cmd = [
                'GUI R',  # open Windows Run
                'DELAY 100',  # wait 100ms
                'STRING cmd',
                'ENTER',
                'DELAY 100',
                'STRING cd Desktop',
                'ENTER',
                'DELAY 100',
                'STRING notepad',
                'ENTER',
                'DELAY 100',
                'F5',
                'ENTER',
            ]
            for e in cmd:
                duck_file.write(e)
                duck_file.write('\n')

            for line in text_file:
                duck_file.write('STRING ' + line)
                duck_file.write('\nENTER\n')

            cmd = [
                'F5',
                'CTRL S',
                'DELAY 100',
                'STRING ' + basename,
                'ENTER',
                'DELAY 50',
                'ALT-F4',
                'DELAY 50',
                'ALT-F4',
            ]
            
            for e in cmd:
                duck_file.write(e)
                duck_file.write('\n')
        
        os.system('sudo raspiducky.py -p ' + duck_filename)
