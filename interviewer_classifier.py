
import os
import random
import numpy as np


# Load wavs belonging to I1
with open ('./annotations/511_diarization.txt', 'r') as f:
    lines = f.readlines()

wavs_i1 = [n[:-3] for n in lines if 'i' in n]

# TODO: maybe add these categories to the classifier
wavs_noise = [n[:-3] for n in lines if 'n' in n]
print('% of noise: ',np.round(len(wavs_noise)/len(lines)*100))
wavs_both = [n[:-3] for n in lines if 'b' in n]
print('% of both: ',np.round(len(wavs_both )/len(lines)*100))

# Load random split of 108
other_wavs = os.listdir('./segmented/108/')
try: other_wavs.remove('.DS_Store')
except: pass
other_wavs.sort()

# move each sample to its own directory
interviewer_dir = './data_interviewers/511_interviewer/'
os.mkdir(interviewer_dir )

wavs_511 = os.listdir('./segmented/511/')
try: wavs_511.remove('.DS_Store')
except: pass
wavs_511.sort()

# obtain filename from segment id
wavs_i1_filename = []
for i in wavs_i1:
    original_filename = [n for n in wavs_511 if i in n]
    try:
        if original_filename:
            wavs_i1_filename.append(original_filename[0])
    except:
        print(i)
        break

os.mkdir('./data_interviewers/511_interviewer/')
for i in wavs_i1_filename:
    os.system('scp ./segmented/511/'+i +' ./data_interviewers/511_interviewer/'+i)

# TODO: here you can manually check these are the interviewer
os.mkdir('./data_interviewers/108_subset/')
# Take subset of other interview
random.shuffle(other_wavs)
for i in other_wavs[:len(wavs_i1)]:
    os.system('scp ./segmented/108/'+i +' ./data_interviewers/108_subset/'+i)


# Train test split
os.mkdir('./data_interviewers/511_interviewer_train/')
os.mkdir('./data_interviewers/511_interviewer_test/')
os.mkdir('./data_interviewers/108_subset_train/')
os.mkdir('./data_interviewers/108_subset_test/')


wavs_511_interviewer = os.listdir('./data_interviewers/511_interviewer/')
random.shuffle(wavs_511_interviewer)
half = int(len(wavs_511_interviewer)/2)
for i in wavs_511_interviewer[:half]:
    os.system('mv ./data_interviewers/511_interviewer/'+i+' ./data_interviewers/511_interviewer_train/')
for i in wavs_511_interviewer[half:]:
    os.system('mv ./data_interviewers/511_interviewer/'+i+' ./data_interviewers/511_interviewer_test/')


wavs_108_subset = os.listdir('./data_interviewers/108_subset/')
random.shuffle(wavs_108_subset )
half = int(len(wavs_108_subset )/2)
for i in wavs_108_subset[:half]:
    os.system('mv ./data_interviewers/108_subset/'+i+' ./data_interviewers/108_subset_train/')
for i in wavs_108_subset[half:]:
    os.system('mv ./data_interviewers/108_subset/'+i+' ./data_interviewers/108_subset_test/')

# Feature extraction
from pyAudioAnalysis import audioTrainTest as aT
aT.featureAndTrain(["./data_interviewers/511_interviewer_train/", "./data_interviewers/108_subset_train/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svmSMtemp", False)

results= []
test_dir = './data_interviewers/108_subset_test/'
for interviewer_sample in os.listdir(test_dir):
    results.append(aT.fileClassification(test_dir+interviewer_sample, "svmSMtemp","svm"))

y_pred = [n[0] for n in results]
import collections
counter=collections.Counter(y_pred)
print(counter)


Result:
(0.0, array([ 0.90156761,  0.09843239]), ['music', 'speech'])


# Train-test split

# Normalization

