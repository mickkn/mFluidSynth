import os
import subprocess
from flask import render_template, send_from_directory
from flask import current_app
from app.main import bp, mfluidsynth

global inst
inst = None


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/', methods=['GET', 'POST'])
def index():
	return render_template('main/index.html')


@bp.route('/fluidsynth/', methods=['GET', 'POST'])
def fluidsynth():

	"""Page with list of sound fonts"""

	sound_fonts = mfluidsynth.Fluidsynth.get_fonts(current_app.config["SF_FOLDER"])

	return render_template('main/fluidsynth.html', soundfonts=sound_fonts)


@bp.route('/fluidsynth/soundfont/<sf>', methods=['GET', 'POST'])
def soundfont(sf):

	"""Load soundfont and display sound banks"""

	global inst

	fs = mfluidsynth.Fluidsynth(path=current_app.config["FS_WIN_EXE"], soundfont=sf)

	inst = fs.get_instruments()

	return render_template('main/soundfont.html', instruments=inst)


@bp.route('/fluidsynth/instrument/<ins>', methods=['GET', 'POST'])
def instrument(ins):

	print(f"Changing instrument to: {ins}")

	mfluidsynth.Fluidsynth.set_instrument(ins)

	return render_template('main/instruments.html', instruments=inst)


@bp.route('/favicon.ico')
def favicon():
	return send_from_directory(
		os.path.join(current_app.root_path, 'static'),
		'favicon.ico',
		mimetype='image/vnd.microsoft.icon'
	)
