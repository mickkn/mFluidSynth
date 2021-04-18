import subprocess
import os
import telnetlib
import sys
import time

FLUIDSYNTH_DEFAULT_ARGS = {

    # "-a": "alsa",   # The name of the audio driver to use. Valid values: dsound, file, wasapi, waveout
    # "-c": "",   # Number of audio buffers
    "-C": "0",  # Turn the chorus on or off [0|1|yes|no, default = on]
    # "-D": "",   # Probe all available soundcards for supported modes, sample-rates and sample-formats.
    # "-d": "",   # Dump incoming and outgoing MIDI events to stdout
    # "-E": "",   # Audio file endian for fast rendering or aufile driver ("help" for list)
    # "-f": "",   # Load command configuration file (shell commands)
    # "-F": "",   # Render MIDI file to raw audio data and store in [file]
    "-g": "1",  # Set the master gain [0 < gain < 10, default = 0.2]
    # "-G": "",   # Defines the number of LADSPA audio nodes
    # "-h": "",   # Print out this help summary
    #"-i": "",   # Don't read commands from the shell [default = yes]
    # "-j": "",   # Attempt to connect the jack outputs to the physical ports
    # "-K": "",   # The number of midi channels [default = 16]
    # "-L": "",   # The number of stereo audio channels [default = 1]
    # "-m": "alsa_seq",   # The name of the midi driver to use. Valid values: winmidi
    # "-n": "",   # Don't create a midi driver to read MIDI input events [default = yes]
    #"-o": "shell.port=9800",  # Define a setting, -o name=value ("-o help" to dump current values)
    # "-O": "",   # Audio file format for fast rendering or aufile driver ("help" for list)
    "-p": " fluid",  # Set MIDI port name (alsa_seq, coremidi drivers)
    #"-q": "",   # Do not print welcome message or other informational output
    # (Windows only: also suppress all log messages lower than PANIC
    "-r": "48000",  # Set the sample rate
    "-R": "0",  # Turn the reverb on or off [0|1|yes|no, default = on]
    #"-s": "",  # Start FluidSynth as a server process
    # "-T": "",   # Audio file type for fast rendering or aufile driver ("help" for list)
    #"-v": "",   # Print out verbose messages about midi events (synth.verbose=1) as well as other debug messages
    # "-V": "",   # Show version of program
    # "-z": "",   # Size of each audio buffer

}

global fluidsynth
fluidsynth = None


class Fluidsynth:

    def __init__(self, path: str = "fluidsynth", soundfont: str = "", arguments: dict = None) -> None:

        global fluidsynth

        self.path = path

        self.arguments_dict = FLUIDSYNTH_DEFAULT_ARGS
        self.arguments = ""

        self.instruments = None

        for name, value in list(self.arguments_dict.items()):
            self.arguments = self.arguments + f" {name}{value}"

        self.arguments = self.arguments + " " + '"' + soundfont + '"'

        if fluidsynth is not None:
            print("Killing old process")
            self.kill_command_windows(fluidsynth.pid)

        print("mdebug:    Starting subprocess")
        print(f"mdebug:    Soundfont: {soundfont}")
        print(f"mdebug:    Args: {self.arguments}")

        fluidsynth = subprocess.Popen(args=self.arguments,
                                      executable=self.path,
                                      universal_newlines=True,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)

    @staticmethod
    def get_fonts(directory):

        sound_fonts = []

        for root, dirs, files in os.walk(directory, topdown=False):
            for filename in files:
                if filename.endswith(".sf2"):
                    sound_fonts.append([os.path.join(root, filename), filename])

        return sound_fonts

    @staticmethod
    def _put(command: str) -> None:
        if not fluidsynth.stdin:
            raise BrokenPipeError()
        fluidsynth.stdin.write(f"{command}\n")
        fluidsynth.stdin.flush()

    def get_instruments(self):

        """ Get a list of instruments """

        # Read all instruments from Soundfont (2 times to get a '> ' end(start) operator)
        self._put("inst 1")
        self._put("inst 1")

        # Reset instrument list
        self.instruments = []

        # Be able to break the freaking stdout.
        breaker = 0
        fluidsynth.stdout.flush()
        for line in fluidsynth.stdout:
            if "> " in line:
                breaker += 1
            if breaker >= 2:
                break
            if "000-" in line and "Copyright" not in line:
                self.instruments.append(line.replace("> ", ""))

        return self.instruments

    @staticmethod
    def set_instrument(instrument: str = ""):

        """ Set instrument of the soundfont loaded """

        cmd_list = []

        print(f"instrument {instrument}")
        ins = int(instrument[4:7])

        # Just add the instrument to all channels
        for i in range(16):
            if i != 9:
                cmd_list.append(f"select {i} 1 0 {ins}")

        for item in cmd_list:
            fluidsynth.stdin.write(f"{item}\n")
            fluidsynth.stdin.flush()

    @staticmethod
    def kill_command_windows(pid):

        """Run command via subprocess"""
        dev_null = open(os.devnull, 'w')
        command = ['TASKKILL', '/F', '/T', '/PID', str(pid)]
        proc = subprocess.Popen(command, stdin=dev_null, stdout=sys.stdout, stderr=sys.stderr)
        proc.communicate()
