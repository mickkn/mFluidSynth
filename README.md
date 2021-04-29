# mFluidSynth
This is a flask webserver, serving fluidsynth for changing soundfont and choose instruments.

The project is running or has been tested on Windows 10 and Raspberry Pi 3B ARMv7

## Dependensies
This project runs through Python 3 and tested/written in version 3.9

Windows:
Install Python 3.9 with pip
Download fluidsynth from https://www.fluidsynth.org/ and install it somewhere you can find.

Linux (Raspberry):
sudo apt-get install python3 python3-pip fluidsynth

Both:
pip install -r requirements.txt

## Setup

* Make a .env file with the content from the .env-example

FS_EXE=fluidsynth
* Executable of fluidsynth, for windows it will be the full path to fluidsynth.exe

SF_FOLDER=/home/pi/soundfonts/
* Folder with soundfonts in .sf2 format

LINUX_ACONN_MIDI=Keystation 49 MK3
* This is the name of your MIDI controller, only used in Linux, and the name can be found via 'aconnect -l'