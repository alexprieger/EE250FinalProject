import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import os
import sys

# MAX_FRQ cannot be safely changed, because get_peak_frqs depends on this value staying 2000
MAX_FRQ = 2000
TONE_LENGTH = 0.1   #seconds
STOP_LENGTH = 0.1   #seconds

LOWER_FRQS = [697, 770, 852, 941]
HIGHER_FRQS = [1209, 1336, 1477]
FRQ_THRES = 20
NUMBER_DIC = {'1' : [LOWER_FRQS[0], HIGHER_FRQS[0]],
              '2' : [LOWER_FRQS[0], HIGHER_FRQS[1]],
              '3' : [LOWER_FRQS[0], HIGHER_FRQS[2]],
              '4' : [LOWER_FRQS[1], HIGHER_FRQS[0]],
              '5' : [LOWER_FRQS[1], HIGHER_FRQS[1]],
              '6' : [LOWER_FRQS[1], HIGHER_FRQS[2]],
              '7' : [LOWER_FRQS[2], HIGHER_FRQS[0]],
              '8' : [LOWER_FRQS[2], HIGHER_FRQS[1]],
              '9' : [LOWER_FRQS[2], HIGHER_FRQS[2]],
              '*' : [LOWER_FRQS[3], HIGHER_FRQS[0]],
              '0' : [LOWER_FRQS[3], HIGHER_FRQS[1]],
              '#' : [LOWER_FRQS[3], HIGHER_FRQS[2]]}

def get_max_frq(frq, fft):
    max_frq = 0
    max_fft = 0
    for idx in range(len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq

def get_peak_frqs(frq, fft):
    #get the high and low frequency by splitting it in the middle (1000Hz)
    hz1000Idx = int(MAX_FRQ * TONE_LENGTH / 2)
    hz650Idx = int(hz1000Idx * 65 / 100)
    hz1500Idx = int(hz1000Idx * 150 / 100)
    low_frq = frq[hz650Idx:hz1000Idx]
    low_frq_fft = fft[hz650Idx:hz1000Idx]

    high_frq = frq[hz1000Idx:hz1500Idx]
    high_frq_fft = fft[hz1000Idx:hz1500Idx]

    return (get_max_frq(low_frq, low_frq_fft), get_max_frq(high_frq, high_frq_fft))

def get_number_from_frq(lower_frq, higher_frq):
    for x in NUMBER_DIC:
        low_f = NUMBER_DIC[x][0]
        high_f = NUMBER_DIC[x][1]
        
        if (lower_frq > (low_f - FRQ_THRES)) and (lower_frq < (low_f + FRQ_THRES)) and (higher_frq > (high_f - FRQ_THRES) and higher_frq < (high_f + FRQ_THRES)):
              
    #return the corresponding key otherwise return '?' if no match is found
            return x
    return '?'

# Checks whether sub is a sublist of lst
def is_sub(sub, lst):
    ln = len(sub)
    for i in range(len(lst) - ln + 1):
        if all(sub[j] == lst[i+j] for j in range(ln)):
            return True
    return False

def main(file, key):
    global SLICE_SIZE
    global WINDOW_SIZE

    key = list(key)
    print("Importing {}".format(file))
    audio = AudioSegment.from_wav(file)

    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate * 1
    samples = audio.get_array_of_samples()

    print("Number of channels: " + str(audio.channels))
    print("Sample count: " + str(sample_count))
    print("Sample rate: " + str(sample_rate))
    print("Sample width: " + str(audio.sample_width))
    print('Length of samples tuple ' + str(len(samples)))

    period = 1 / sample_rate                     #the period of each sample
    duration = sample_count / sample_rate         #length of full audio in seconds
    slice_sample_size = int(TONE_LENGTH*sample_rate)   #get the number of elements expected for TONE_LENGTH seconds


    #generating the frequency spectrum
    k = np.arange(slice_sample_size)                                #k is an array from 0 to [n] with a step of 1
    frq = k/TONE_LENGTH                          #generate the frequencies by dividing every element of k by slice_duration

    max_frq_idx = int(MAX_FRQ * TONE_LENGTH)       #get the index of the maximum frequency (2000)
    frq = frq[range(max_frq_idx)]                   #truncate the frequency array so it goes from 0 to 2000 Hz

    start_index = 0 #set the starting index at 0
    output = []
    while start_index <= sample_count - TONE_LENGTH: #end_index < len(samples):
        end_index = start_index + slice_sample_size      #find the ending index for the slice

        print("Start index: %d, end index: %d" % (start_index, end_index))
        sample_slice = samples[start_index:end_index]
        sample_slice_fft = np.fft.fft(sample_slice)/slice_sample_size
        sample_slice_fft = sample_slice_fft[range(max_frq_idx)]
        print("Max frq: %d, max frq index: %d" % (frq[max_frq_idx - 1], max_frq_idx))
        
        peaks = get_peak_frqs(frq, sample_slice_fft)

        print("Peaks: " + str(peaks))
        num_received = get_number_from_frq(peaks[0], peaks[1])
        output.append(num_received)
        
        start_index += int((TONE_LENGTH + STOP_LENGTH) * sample_rate)

    print("Key: " + str(key) + " with type " + str(type(key)))
    print("Decoded input: " + str(output))
    if(is_sub(key, output)):
        return True
    else:
        return False
        

if __name__ == '__main__':
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        print("Usage: decode.py [file] [key]")
        exit(1)
    access = main(sys.argv[1], sys.argv[2])
    if(access):
        print("ACCESS GRANTED")
    else:
        print("ACCESS DENIED")
