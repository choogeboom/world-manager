from flask.blueprints import Blueprint

from world_manager.blueprints.user.decorators import anonymous_required

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    pass
