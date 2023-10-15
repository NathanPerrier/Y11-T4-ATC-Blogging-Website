from backend.config import *
from backend.wraps.__init__ import *
from backend.db import db
from backend.authentication.reset_code import ResetCode
from backend.authentication.user import User

forgot = Blueprint('forgot', __name__)

TITLE = 'Ambrose Treacy College'

@forgot.route('/forgot password', methods=['GET', 'POST']) 
def forgot_password(error=''):
    return render_template('forgot_password.html', title=TITLE, error=error)  

@forgot.route('/forgot password/validate_email', methods=['POST'])
def validate_email():
    valid, error = ResetCode.create_and_send_reset_code(request.form.get('email'))
    return jsonify(success=valid, error=error)

@forgot.route('/forgot password/validate_code', methods=['POST'])
def validate_code():
    valid, error = ResetCode.check_reset_code(request.form.get('email'), request.form.get('reset_code'))
    return jsonify(success=valid, error=error)

@forgot.route('/forgot password/validate_password', methods=['POST'])
def validate_password():
    valid, error = User.change_password(request.form.get('email'), request.form.get('new_password'))
    if valid: 
        ResetCode.delete_by_user_id(db, User().get_by_email(db, request.form.get('email')).id)
        session['confirmed_access_confirmed'] = True
    return jsonify(success=valid, error=error)


@forgot.route('/forgot password/confirmed')
@confirmed_page_access
def password_confirmed():
    return redirect('/')