from flask.blueprints import Blueprint
from flask.templating import render_template

char = Blueprint('char', __name__,
                 template_folder='templates',
                 url_prefix='/char')


@char.route('/flinty')
def flinty():
    return render_template('char/flinty.html')
