import subprocess
import os
import telnetlib
import sys

FLUIDSYNTH_DEFAULT_ARGS = {

    #"-a": "alsa",   # The name of the audio driver to use. Valid values: dsound, file, wasapi, waveout
    #"-c": "",   # Number of audio buffers
    "-C": "0",   # Turn the chorus on or off [0|1|yes|no, default = on]
    #"-D": "",   # Probe all available soundcards for supported modes, sample-rates and sample-formats.
    #"-d": "",   # Dump incoming and outgoing MIDI events to stdout
    #"-E": "",   # Audio file endian for fast rendering or aufile driver ("help" for list)
    #"-f": "",   # Load command configuration file (shell commands)
    #"-F": "",   # Render MIDI file to raw audio data and store in [file]
    #"-g": "",   # Set the master gain [0 < gain < 10, default = 0.2]
    #"-G": "",   # Defines the number of LADSPA audio nodes
    #"-h": "",   # Print out this help summary
    #"-i": " ",   # Don't read commands from the shell [default = yes]
    #"-j": "",   # Attempt to connect the jack outputs to the physical ports
    #"-K": "",   # The number of midi channels [default = 16]
    #"-L": "",   # The number of stereo audio channels [default = 1]
    #"-m": "alsa_seq",   # The name of the midi driver to use. Valid values: winmidi
    #"-n": "",   # Don't create a midi driver to read MIDI input events [default = yes]
    "-o": "shell.port=9800",   # Define a setting, -o name=value ("-o help" to dump current values)
    #"-O": "",   # Audio file format for fast rendering or aufile driver ("help" for list)
    "-p": " fluid",   # Set MIDI port name (alsa_seq, coremidi drivers)
    #"-q": "",   # Do not print welcome message or other informational output
                # (Windows only: also suppress all log messages lower than PANIC
    "-r": "48000",   # Set the sample rate
    "-R": "0",   # Turn the reverb on or off [0|1|yes|no, default = on]
    "-s": "",   # Start FluidSynth as a server process
    #"-T": "",   # Audio file type for fast rendering or aufile driver ("help" for list)
    #"-v": "",   # Print out verbose messages about midi events (synth.verbose=1) as well as other debug messages
    #"-V": "",   # Show version of program
    #"-z": "",   # Size of each audio buffer

}


class Fluidsynth:

    def __init__(self, path: str = "fluidsynth", arguments: dict = None) -> None:

        self.path = path

        self.arguments_dict = FLUIDSYNTH_DEFAULT_ARGS
        self.arguments = ""

        self.running = False

        self.fluidsynth = None

    def start_process(self, soundfont):

        self.arguments = ""

        for name, value in list(self.arguments_dict.items()):
            self.arguments = self.arguments + f" {name}{value}"

        self.arguments = self.arguments + " " + '"' + soundfont + '"'

        if self.fluidsynth is not None:
            self.kill_command_windows(self.fluidsynth.pid)

        self.fluidsynth = subprocess.Popen(args=self.arguments, executable=self.path)
        print(self.fluidsynth.poll())
        self.fluidsynth.wait()

    def get_fonts(self, directory):

        sound_fonts = []

        for root, dirs, files in os.walk(directory, topdown=False):
            for filename in files:
                if filename.endswith(".sf2"):
                    sound_fonts.append([os.path.join(root, filename), filename])

        return sound_fonts

    def read_write(self, command: str) -> None:

        output = self.fluidsynth.communicate(command.encode('ascii') + b"\n")

        if type(output) is tuple:
            return ""
        else:
            return output.decode('ascii')

    def get_banks(self):

        print("get_instruments")
        #self.fluidsynth.stdin.flush()
        #self.fluidsynth.stdin.write("inst 1".encode('ascii') + b"\n")
        #self.fluidsynth.stdin.write("inst 1".encode('ascii') + b"\n")
        #print(self.fluidsynth.communicate()[0])
        #print(self.fluidsynth.stdout.read().decode("ascii"))

        #output = self.fluidsynth.communicate("inst 1\n".encode('ascii'))
        #print(output)
        #print(self.read_write("inst 1"))

        #self.fluidsynth.stdin.write('inst 1\n'.encode('ascii'))
        #self.fluidsynth.stdin.close()
        #result = self.fluidsynth.stdout.read()
        #print(result.decode('ascii'))

        #self.fluidsynth.stdin.write('inst 1\n'.encode('ascii'))
        #self.fluidsynth.stdin.close()
        #result = self.fluidsynth.stdout.read()
        #print(result)

        tn = telnetlib.Telnet("localhost", 9800)
        tn.read_until('> '.encode('ascii'))
        tn.write("inst 1\r\n".encode('ascii'))
        instruments = tn.read_until('> '.encode('ascii')).decode('ascii')
        #instruments.replace("b'", "").replace("> '", "")
        instruments.split("\n")
        print(instruments)

        #tn.write("inst 1\n")
        #print(tn.read_lazy().decode('ascii'))
        #tn.close()

    def kill_command_windows(self, pid):

        """Run command via subprocess"""
        dev_null = open(os.devnull, 'w')
        command = ['TASKKILL', '/F', '/T', '/PID', str(pid)]
        proc = subprocess.Popen(command, stdin=dev_null, stdout=sys.stdout, stderr=sys.stderr)