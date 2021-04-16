import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ZJpoasj187321+07!Jidaspj'

    STATIC_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static')

    FS_WIN_EXE = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              'fluidsynth-2.2.0-win10-x64', 'bin', 'fluidsynth.exe')
    FS_LINUX_EXE = "fluidsynth"

    SF_FOLDER = r"C:\Users\mk\Desktop\soundfonts"
    #os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fluidsynth-2.2.0-win10-x64', 'bin')
