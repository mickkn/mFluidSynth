#!/usr/bin/env bash
FLASK_APP=main.py
FLASK_DEBUG=1
source /home/pi/mFluidSynth/venv/bin/activate
flask run --host=0.0.0.0 --port=5050