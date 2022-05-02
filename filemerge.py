import audioop
from pydub import AudioSegment
import os
import sys

def main(file):
    print("Importing {}".format(file))
    file1 = AudioSegment.from_wav(file)

    os.system("ssh nate@20.125.112.134")
    

if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print('Usage : decode.py [file]')
        exit(1)
    main(sys.argv[1])