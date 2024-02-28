from backend.config import *
from backend.forms.__init__ import *
from backend.wraps.__init__ import *
from backend.authentication.user import User

from backend.ai.text_completion import *

main = Blueprint('main', __name__)

TITLE = 'Ambrose Treacy College'

@main.route('/',  methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def index(): 
    # print(TextCompletion().suggest_word('The quick b'))
    # print(TextCompletion().suggest_word('The quick brown f'))
    # print(TextCompletion().suggest_word('The quick brown fox'))
    # print(TextCompletion().suggest_word('The q'))  
    return render_template('index.html', title=TITLE, user=current_user)

@main.route('/erea', methods=['GET', 'POST'])
def erea():
    return render_template('erea.html', title=TITLE, user=current_user)

@main.route('/login', methods=['GET', 'POST'])
def login(error=''):
    form=LoginForm()
    next=request.args.get('next')
    if request.method == 'POST': error = User().login()
    if current_user.is_authenticated: return redirect(next) if next else redirect(url_for('main.index'))
    return render_template('login.html', title=TITLE, error=error, form=form, theme=True, next=next)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/handle-contact-request', methods=['POST'])
@handle_contact_request
def handle_contact_request():
     return jsonify({'message': 'POST request received'}), 200
 
@main.route('/handle-newsletter', methods=['POST'])
@handle_newsletter
def handle_newsletter():
     return jsonify(success=True, error=None), 200
 
