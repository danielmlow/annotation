# Diarization annotator

Listen to interview 511_7min.wav for a couple of minutes to get acquainted with interviewer and participant’s voices
Open terminal
Go to folder annotation:
```cd ./path/to/annotation/```

To install, follow these steps:

```python -m venv env```

```source env/bin/activate```

```pip install -r requirements.txt```



Run script in terminal:

```source env/bin/activate```

```python annotate_diarization.py --511 --0```

```deactivate```

Instructions:
```>>> Who is speaking: i, p, b, n, r?``` 
Where i=interviewer, p=participant, b=both, n=not clear/noise, r = repeat
Enter q to quit. Pay attention to the message: (replace 0 above in 5.a. if instructed to after quitting). For example:
```=====You quit midway. Restart on file 10=====```

To resume write the following in terminal:
```python annotate_diarization.py --511 --N```
Where N is the number it instructed. For example:
```python annotate_diarization.py --511 --10```

Send me these outputs that will be inside ./annotation/
./annotation/511_diarization.txt
./annotation/511_log

Deactivate from virtual environment in terminal
```deactivate```

---



# Evaluate diarization on annotated interviewer (1) and random snippets from other interview (0)

interviewer_classifier.py

Once you obtain an annotation for fileX.wav, goal is to train classifier to detect interviewer I1 in fileX.wav
Segment a different interview with different interviewer and speaker into wavs

Feature extraction and normalization on wavs

Training data: 
* 1 = half of I1 511
* 0: random snippets from second interview 108

Test data A
* 1 = other half of I1 511
* 0: random snippets from second interview 108

Test data B
Annotate a I1 samples from a third interview 509
* 1 = I1 samples from a third interview 509
* 0: random snippets from second interview 108


