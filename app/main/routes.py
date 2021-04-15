import os
import subprocess
from flask import render_template, send_from_directory
from flask import current_app
from app.main import bp, mfluidsynth


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/', methods=['GET', 'POST'])
def index():
	return render_template('main/index.html')


@bp.route('/fluidsynth/', methods=['GET', 'POST'])
def fluidsynth():

	fs_exe = os.path.join(current_app.config["FS_WIN_FOLDER"], "fluidsynth.exe")

	fluidsynth_obj = mfluidsynth.Fluidsynth(path=fs_exe)

	fluidsynth_obj.start_process('"C:\\Users\\mk\\Desktop\\soundfonts\\Essential Keys-SF-v1.3.sf2"')

	return render_template('main/fluidsynth.html')


@bp.route('/favicon.ico')
def favicon():
	return send_from_directory(
		os.path.join(current_app.root_path, 'static'),
		'favicon.ico',
		mimetype='image/vnd.microsoft.icon'
	)
