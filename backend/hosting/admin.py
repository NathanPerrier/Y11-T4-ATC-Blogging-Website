from django.core.paginator import Paginator
from backend.config import *
from backend.forms.add_user import AddUserForm
from backend.forms.manage_account import *
from backend.authentication.user import User
from backend.blog.blog import Blog
from backend.db import db


admin = Blueprint('admin', __name__)

TITLE = 'Ambrose Treacy College'


@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    if current_user.admin:
        return render_template('admin/admin.html', title=TITLE, user=current_user)
    return abort(401)

@admin.route('/admin/users', methods=['GET', 'POST'])
@login_required
def admin_users():
    paginator = Paginator(User.get_all(db), 10)
    page = request.args.get('page')
    users = paginator.get_page(page)
    if current_user.admin:
        return render_template('admin/user_management.html', title=TITLE, user=current_user, users=users)
    return abort(401)


@admin.route('/admin/add', methods=['GET', 'POST'])
@login_required
def admin_add_user(error=''):
    if current_user.admin:
        form = AddUserForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                if User().get_by_email(db, form.email.data) is None:
                    User().add_user(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
                    return redirect(url_for('admin.admin_users'))
                else: error='User already exists'
            else: error='Invalid Input Feild(s)'
        return render_template('admin/add_user.html', title=TITLE, user=current_user, form=form, error=error)
    return abort(401)


@admin.route('/admin/<int:user_id>/manage', methods=['GET', 'POST'])
@login_required
def admin_manage_user(user_id):
    if current_user.admin:
        user = User().get_by_id(db, user_id)   
        try: 
            error = session['error']
            session.pop('error', None)
        except: error = ''
        return render_template('admin/manage_user_account.html', title=TITLE, user=current_user, _user_=user, address=user.address, bio=user.bio, error=error, formAccount=UpdateAccountForm(), formPassword=UpdatePasswordForm(), formPicture=UpdatePictureForm()) 
    return abort(401)


@admin.route('/admin/<int:user_id>/manage/update', methods=['POST'])
@login_required
def validate_account_update(user_id, error=''):
    if current_user.admin:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            error = User().update_account(User().get_by_id(db, user_id), form.first_name.data, form.last_name.data, form.email.data, form.username.data, form.phone_number.data, form.street_number.data, form.street_name.data, form.suburb.data, form.postcode.data, form.bio.data)
        else: error='Invalid Form Input(s)'
        print(error)
        session['error'] = error
        return redirect('/admin/'+str(user_id)+'/manage')
    return abort(401)

@admin.route('/account/<int:user_id>/manage/password/update', methods=['POST']) 
@login_required
def validate_password_update(user_id, error=''):
    if current_user.admin:
        form = UpdatePasswordForm()
        if form.validate_on_submit():
            user = User().get_by_id(db, user_id)
            if User().check_password(user.password, form.old_password.data):
                valid, error = User().change_password(user.email, form.new_password.data)
            else: error = 'Incorrect Password'
        else: error='Invalid Form Input(s)'
        flash(error, "error")
        return redirect('/admin/'+str(user_id)+'/manage')
    return abort(401)

@admin.route('/account/<int:user_id>/manage/picture/update', methods=['POST'])
@login_required
def validate_picture_update(user_id, error=''):
    if current_user.admin:
        form = UpdatePictureForm() 
        if form.validate_on_submit():
            print(form.picture.data, form.checkbox.data)
            success, error = User().save_user_avatar(User().get_by_id(db, user_id), form.picture.data, form.checkbox.data)
        else: error='Invalid Form Input(s)'
        flash(error, "error-2")
        return redirect('/admin/'+str(user_id)+'/manage')
    return abort(401)

@admin.route('/admin/<int:user_id>/manage/picture/restore', methods=['GET', 'POST'])
@login_required
def restore_picture(user_id):
    if current_user.admin:
        User().restore_user_avatar(User().get_by_id(db, user_id))
        return redirect('/admin/'+str(user_id)+'/manage')
    return abort(401)


@admin.route('/admin/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def admin_delete_user(user_id):
    if current_user.admin:
        User().delete_user(db, user_id)   # Delete user
        return redirect(url_for('admin.admin_users'))
    return abort(401)

@admin.route('/account/<int:user_id>/manage/delete', methods=['GET'])
@login_required
def delete_account(user_id):
    if current_user.admin:
        User().delete_user(db, user_id)
        return redirect(url_for('admin.admin_users'))
    return abort(401)  