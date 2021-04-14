import os
from flask import render_template, send_from_directory
from flask import current_app
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/', methods=['GET', 'POST'])
def index():
	return render_template('main/index.html', title='Home')


@bp.route('/favicon.ico')
def favicon():
	return send_from_directory(
		os.path.join(current_app.root_path, 'static'),
		'favicon.ico',
		mimetype='image/vnd.microsoft.icon'
	)
