import subprocess

FLUIDSYNTH_DEFAULT_ARGS = {

    #"-a": "",   # The name of the audio driver to use. Valid values: dsound, file, wasapi, waveout
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
    "-i": " ",   # Don't read commands from the shell [default = yes]
    #"-j": "",   # Attempt to connect the jack outputs to the physical ports
    #"-K": "",   # The number of midi channels [default = 16]
    #"-L": "",   # The number of stereo audio channels [default = 1]
    #"-m": "",   # The name of the midi driver to use. Valid values: winmidi
    #"-n": "",   # Don't create a midi driver to read MIDI input events [default = yes]
    #"-o": "",   # Define a setting, -o name=value ("-o help" to dump current values)
    #"-O": "",   # Audio file format for fast rendering or aufile driver ("help" for list)
    "-p": " fluid",   # Set MIDI port name (alsa_seq, coremidi drivers)
    #"-q": "",   # Do not print welcome message or other informational output
                # (Windows only: also suppress all log messages lower than PANIC
    "-r": "48000",   # Set the sample rate
    "-R": "0",   # Turn the reverb on or off [0|1|yes|no, default = on]
    "-s": "",   # Start FluidSynth as a server process
    #"-T": "",   # Audio file type for fast rendering or aufile driver ("help" for list)
    "-v": "",   # Print out verbose messages about midi events (synth.verbose=1) as well as other debug messages
    #"-V": "",   # Show version of program
    #"-z": "",   # Size of each audio buffer

}


class Fluidsynth:

    def __init__(self, path: str = "fluidsynth", arguments: dict = None) -> None:

        self.path = path

        self.arguments_dict = FLUIDSYNTH_DEFAULT_ARGS
        self.arguments = ""

        self.fluidsynth = None

    def start_process(self, soundfont):

        self.arguments = ""

        for name, value in list(self.arguments_dict.items()):
            self.arguments = self.arguments + f" {name}{value}"

        self.arguments = self.arguments + " " + soundfont

        print(self.arguments)

        if self.fluidsynth is not None:
            self.fluidsynth.kill()

        self.fluidsynth = subprocess.Popen(self.path + self.arguments)

    def get_fonts(self):

        print("do something")

    def __del__(self) -> None:

        if self.fluidsynth is not None:
            self.fluidsynth.kill()
