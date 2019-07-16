#!/usr/bin/env python3

'''
Author: Daniel M. Low (Harvard U.-MIT)
'''



import pygame
import os
import sys
import re


participant = sys.argv[1][2:]
input_dir = './segmented/'+participant+'/'
output_dir = './'
# output_dir = './'
# output_filename = 'diarization.txt'




def sync_playback(filename):
    # takes in a file and plays it back 
    pygame.mixer.init(16000)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

# import pyaudio
# import wave

# def play_wav(filepath):
#
#
#     # define stream chunk
#     chunk = 1024
#
#     # open a wav format music
#     f = wave.open(filepath, "rb")
#     # instantiate PyAudio
#     p = pyaudio.PyAudio()
#     # open stream
#     stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
#                     channels=f.getnchannels(),
#                     rate=f.getframerate(),
#                     output=True)
#     # read data
#     data = f.readframes(chunk)
#
#     # play stream
#     while data:
#         stream.write(data)
#         data = f.readframes(chunk)
#
#         # stop stream
#     stream.stop_stream()
#     stream.close()
#
#     # close PyAudio
#     p.terminate()


def main(i = 0, files = None, output_path = None, output_dir = None):
    response = 'x'
    while (len(files) >= i and response.lower() != 'q'):
            print("Who is speaking: i, p, b, n, r? ")
            # 1. play audio
            # play_wav(files[i])
            sync_playback(files[i])

            # receive input
            response = input()
            # Repeat:
            if response.lower() == 'r':
                sync_playback(files[i])
                response = input()
            # Log answer:
            elif response.lower() == 'i' or response.lower() == 'p' or response.lower() == 'b' or response.lower() == 'n':
                i += 1
                file = files[i]
                segment = re.search('17_(.*)_segmented', file).group(1)
                with open(output_path, 'a+') as f:
                    f.write(str(segment)+','+response+'\n')
            elif response.lower() == 'q':
                if response.lower() == 'q':
                    with open(output_path, 'a+') as f:
                        f.write('===,===\n')
                    print('You quit midway. Restart on file %d by running: python annotate_diarization.py --511 --%d \n' % (i,i))
                    with open(output_dir + participant +'_log.txt', 'a+') as f:
                        f.write('You quit midway. Restart on file %d by running: python annotate_diarization.py --511 --%d \n' % (i,i))
                break
            # Incorrect answer, repeat:
            else:
                print(response, ' is not a viable answer. Please correct:')
                print("Who is speaking: i, p, b, n, r? ")
                sync_playback(files[i])
                response = input()
    if i==len(files) and len(files) == os.system('wc -l < '+participant+'_diarization.txt'):
        print('You finished. Looks good.')
        with open(output_dir + participant+'_log.txt', 'a+') as f:
            f.write('<Looks good: len of files == wc -l < '+participant+'_diarization.txt>'+'\n')
    elif i==len(files) and len(files) != os.system('wc -l < '+participant+'_diarization.txt'):
        print('You finished. I need to review.')
        with open(output_dir +participant+'_log.txt', 'a+') as f:
            f.write('You finished. I need to review.')
    return





output_filename = participant+'_diarization.txt'
output_path = output_dir+output_filename

if not os.path.exists(os.path.dirname(output_dir)):
    try:
        os.makedirs(os.path.dirname(output_dir))
    except:
        print('error creating directory')


files = os.listdir(input_dir)
try: files.remove('.DS_Store')
except: pass

files.sort()
files = [input_dir+file for file in files]

i = int(sys.argv[2][2:])
main(i = i, files = files, output_path = output_path, output_dir = output_dir)
