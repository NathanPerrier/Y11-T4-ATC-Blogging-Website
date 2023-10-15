from backend.config import *
from backend.wraps.__init__ import *
from backend.authentication.signup_code import SignupCode
from backend.authentication.user import User

sign_up = Blueprint('sign_up', __name__)

TITLE = 'Ambrose Treacy College'

@sign_up.route('/signup', methods=['GET', 'POST']) 
def signup_page(error=''):
    return render_template('signup.html', title=TITLE, error=error) 

@sign_up.route('/signup/validate_email', methods=['POST'])   #! issue
def signup_validate_email():
    valid, error = SignupCode.create_and_send_reset_code(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'))
    return jsonify(success=valid, error=error)

@sign_up.route('/signup/validate_code', methods=['POST'])
def signup_validate_code():
    valid, error = SignupCode.check_reset_code(request.form.get('email'), request.form.get('reset_code'))
    return jsonify(success=valid, error=error)

@sign_up.route('/signup/validate_password', methods=['POST'])
def signup_validate_password():
    valid, error = User.signup(request.form.get('first_name'),request.form.get('last_name'), request.form.get('email'), request.form.get('new_password'))
    return jsonify(success=valid, error=error)
