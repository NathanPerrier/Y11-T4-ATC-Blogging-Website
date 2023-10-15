from backend.config import *
from backend.authentication.user import User

subject = Blueprint('subject', __name__)

TITLE = 'Ambrose Treacy College'

@subject.route('/subjects', methods=['GET', 'POST'])
def subjects():
    return render_template('subjects.html', title=TITLE, user=current_user)

@subject.route('/subjects/english', methods=['GET', 'POST'])
def english():
    return render_template('subjects/english.html', title=TITLE, user=current_user)

@subject.route('/subjects/maths', methods=['GET', 'POST'])
def maths():
    return render_template('subjects/maths.html', title=TITLE, user=current_user)

@subject.route('/subjects/technology', methods=['GET', 'POST'])
def technology():
    return render_template('subjects/technology.html', title=TITLE, user=current_user)

@subject.route('/subjects/science', methods=['GET', 'POST'])
def science():
    return render_template('subjects/science.html', title=TITLE, user=current_user)

@subject.route('/subjects/religion', methods=['GET', 'POST'])
def relgion():
    return render_template('subjects/religion.html', title=TITLE, user=current_user)

@subject.route('/subjects/music', methods=['GET', 'POST'])
def music():
    return render_template('subjects/music.html', title=TITLE, user=current_user)