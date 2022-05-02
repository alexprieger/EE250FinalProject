import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import os
import sys

#http://dialabc.com/sound/generate/index.html?pnum=1234&auFormat=wavpcm44&toneLength=300&mtcontinue=Generate+DTMF+Tones

MAX_FRQ = 2000
SLICE_SIZE = 0.15 #seconds
WINDOW_SIZE = 0.175 #seconds

# TODO: implement this dictionary              
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
            #print(abs(fft[idx]))
            #rint(frq[idx])
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq

def get_peak_frqs(frq, fft):
    #TODO: implement an algorithm to find the two maximum values in a given array

    #get the high and low frequency by splitting it in the middle (1000Hz)
    low_frq = frq[90:150]
    low_frq_fft = fft[90:150]
    print("low_frq : " + str(frq[90]) + " - " + str(frq[150]))

    high_frq = frq[150:300]
    high_frq_fft = fft[150:300] 
    print(len(frq))
    print("high_frq : " + str(frq[150]) + " - " + str(frq[299]))   
    #spliting the FFT to high and low frequencies

    return (get_max_frq(low_frq, low_frq_fft), get_max_frq(high_frq, high_frq_fft))

def get_number_from_frq(lower_frq, higher_frq):
    #TODO: given a lower frequency and higher frequency pair
    print('lower : ' + str(lower_frq))
    print('higher : ' + str(higher_frq))
    print('-------------------------')
    for x in NUMBER_DIC:
        low_f = NUMBER_DIC[x][0]
        high_f = NUMBER_DIC[x][1]
        
        
        if (lower_frq > (low_f - 20)) and (lower_frq < (low_f + 20)) and (higher_frq > (high_f - 20) and higher_frq < (high_f + 20)):
              
    #return the corresponding key otherwise return '?' if no match is found
            return x
    return '?'

def main(file):
    print("Importing {}".format(file))
    audio = AudioSegment.from_mp3(file)

    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate * 2
    samples = audio.get_array_of_samples()
    
    print("Number of channels: " + str(audio.channels))
    print("Sample count: " + str(sample_count))
    print("Sample rate: " + str(sample_rate))
    print("Sample width: " + str(audio.sample_width))

    period = 1/sample_rate                     #the period of each sample
    duration = sample_count/sample_rate         #length of full audio in seconds
    SLICE_SIZE = 0.150  #seconds
    WINDOW_SIZE = 0.175 #seconds
    slice_sample_size = int(SLICE_SIZE*sample_rate)   #get the number of elements expected for [SLICE_SIZE] seconds

    n = slice_sample_size                            #n is the number of elements in the slice

    #generating the frequency spectrum
    k = np.arange(n)                                #k is an array from 0 to [n] with a step of 1
    slice_duration = n/sample_rate                   #slice_duration is the length of time the sample slice is (seconds)
    frq = k/slice_duration                          #generate the frequencies by dividing every element of k by slice_duration

    max_frq_idx = int(MAX_FRQ*slice_duration)       #get the index of the maximum frequency (2000)
    frq = frq[range(max_frq_idx)]                   #truncate the frequency array so it goes from 0 to 2000 Hz

    search = 0
    while (search < sample_count):
        if(abs(samples[search]) > 1500):
            print(search)
            print(search * sample_rate)
            break
        search+=1
    
    start_index = search 
                                    #set the starting index at 0
    end_index = start_index + slice_sample_size      #find the ending index for the slice
    output = ''
    print('start index')
    print(start_index)
    i = 1
    num_idx = 0
    while (i < 5):#end_index < len(samples):
        #print("Sample {}:".format(i))
        i += 1
        print(str(start_index/sample_rate) + ' - ' +str(end_index/sample_rate)) 
        #TODO: grab the sample slice and perform FFT on it
        sample_slice = samples[start_index:end_index]
        sample_slice_fft = np.fft.fft(sample_slice)/n
        #TODO: truncate the FFT to 0 to 2000 Hz
        sample_slice_fft = sample_slice_fft[range(max_frq_idx)]
        #TODO: calculate the locations of the upper and lower FFT peak using get_peak_frqs()
        """
        print("----")
        print("sample size: " + str(len(sample_slice_fft)))
        print("f: " + str(len(frq)))
        #print("fmax" + str(frq[end_index]))
        print("----")
        """
        peaks = get_peak_frqs(frq, sample_slice_fft)

        #TODO: print the values and find the number that corresponds to the numbers
        #print("Peak 1: " + str(peaks[0]) + ", Peak 2: " + str(peaks[1]))
        num_received = get_number_from_frq(peaks[0], peaks[1])
        output += num_received
        #print('Corresponding number : ' + str(output))
        #Incrementing the start and end window for FFT analysis
        print(i)
        if(i > 2):
            WINDOW_SIZE = 0.35
            SAMPLE_SIZE = 0.3
        start_index += int(WINDOW_SIZE*sample_rate)
        slice_sample_size = int(SLICE_SIZE*sample_rate)
        
        end_index = start_index + slice_sample_size

    #print("Program completed")
    print("Decoded input: " + str(output))
    if(output == '1234'):
        print('ACCESS GRANTED')
    else:
        print('ACCESS DENIED')
        

if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print("Usage: decode.py [file]")
        exit(1)
    main(sys.argv[1])
