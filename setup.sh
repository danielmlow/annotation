#!/bin/bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python annotate_diarization.py --511 --0

