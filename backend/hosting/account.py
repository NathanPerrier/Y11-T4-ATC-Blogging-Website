from backend.config import *
from backend.social.social import Social
from backend.forms.manage_account import * 
from backend.authentication.user import User
from backend.data.user_bio import Bio
from backend.data.address import Address
from backend.blog.rating import Rating 
from django.core.paginator import Paginator
from backend.blog.blog import Blog
from backend.db import db


account = Blueprint('account', __name__)

TITLE = 'Ambrose Treacy College'

@account.route('/account', methods=['GET', 'POST']) 
@login_required
def account_page():
    paginator = Paginator(Blog.get_by_user_id(db, current_user.id), 4) 
    page = request.args.get('page')
    blogs = paginator.get_page(page)
    return render_template('account/account.html', title=TITLE, user=current_user, followers=Social.count_followers(db, current_user.id), following=Social.count_following(db, current_user.id), blogs=blogs, num_blogs=len(Blog.get_by_user_id(db, current_user.id)), ratings=Rating().get_all(db),  social=Social().get_all(db)) 

@account.route('/account/manage', methods=['GET', 'POST']) 
@login_required
def manage_account_page():
    try: 
        error = session['error']
        session.pop('error', None)
    except: error = ''
    return render_template('account/manage_account.html', title=TITLE, user=current_user, address=current_user.address, bio=current_user.bio, error=error, formAccount=UpdateAccountForm(), formPassword=UpdatePasswordForm(), formPicture=UpdatePictureForm()) 

@account.route('/account/<string:user_username>', methods=['GET', 'POST'])
def user_account_page(user_username):
    user = User.query.filter_by(username=user_username).first()
    if user:
        if user != current_user:
            paginator = Paginator(Blog.get_by_user_id(db, user.id), 4)
            page = request.args.get('page')
            blogs = paginator.get_page(page)
            return render_template('account/user_account.html', title=TITLE, user=current_user, account=user, followers=Social.count_followers(db, user.id), following=Social.count_following(db, user.id), blogs=blogs, num_blogs=len(Blog.get_by_user_id(db, user.id)), social=Social().get_all(db), ratings=Rating().get_all(db)) 
        return redirect(url_for('account.account_page'))
    return redirect('/404')


@account.route('/account/manage/update', methods=['POST'])
@login_required
def validate_account_update(error=''):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        error = User().update_account(current_user, form.first_name.data, form.last_name.data, form.email.data, form.username.data, form.phone_number.data, form.street_number.data, form.street_name.data, form.suburb.data, form.postcode.data, form.bio.data)
    else: error='Invalid Form Input(s)'
    print(error)
    session['error'] = error
    return redirect(url_for('account.manage_account_page'))


@account.route('/account/manage/password/update', methods=['POST']) 
@login_required
def validate_password_update(error=''):
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if User().check_password(current_user.password, form.old_password.data):
            valid, error = User().change_password(current_user.email, form.new_password.data)
        else: error = 'Incorrect Password'
    else: error='Invalid Form Input(s)'
    flash(error, "error")
    return redirect(url_for('account.manage_account_page'))

@account.route('/account/manage/picture/update', methods=['POST'])
@login_required
def validate_picture_update(error=''):
    form = UpdatePictureForm() 
    if form.validate_on_submit():
        print(form.picture.data, form.checkbox.data)
        success, error = User().save_user_avatar(current_user, form.picture.data, form.checkbox.data)
    else: error='Invalid Form Input(s)'
    flash(error, "error-2")
    return redirect(url_for('account.manage_account_page'))

@account.route('/account/manage/picture/restore', methods=['GET', 'POST'])
@login_required
def restore_picture():
    User().restore_user_avatar(current_user)
    return redirect(url_for('account.manage_account_page'))

@account.route('/account/manage/delete', methods=['GET'])
@login_required
def delete_account():
    User().delete_user(db, current_user.id)
    logout_user()
    return redirect('/')


@account.route('/account/<string:user_username>/follow', methods=['POST'])
@login_required
def follow_blog(user_username):
    user = User().get_by_username(db, user_username)
    Social().follow(db, current_user.id, user.id)
    return jsonify({'success': True})