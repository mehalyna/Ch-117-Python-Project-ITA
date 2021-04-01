import os
import traceback

from bson import ObjectId
from dotenv import load_dotenv
from flask import flash, Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, logout_user, login_user, login_required
from forms import LoginForm, AddUserForm, UpdateUserForm
from models import User
from mongoengine import connect
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
connect(
    db=os.getenv('DB_NAME'),
    host=os.getenv('MONGO_URL'),
    port=int(os.getenv('PORT'))
)
login = LoginManager(app)
login.login_view = 'admin_login'
login.init_app(app)


@app.route('/')
@login_required
def start_page():
    return render_template('index.html')


@app.route('/active_users_list')
@login_required
def get_active_users_list():
    users = User.objects(status='active')
    return render_template('users_list.html', users=users)


@app.route('/inactive_users_list')
@login_required
def get_inactive_users_list():
    users = User.objects(status='inactive')
    return render_template('users_list.html', users=users)


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = AddUserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = User(email=form.email.data)
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.login = form.login.data
            user.set_password(form.password.data)
            user.role = form.role.data
            user.status = 'active'
            user.save()
            flash('User successfully created', 'success')
            return redirect(url_for('get_active_users_list'))
        except Exception as e:
            print("Something went wrong!")
            traceback.print_exc()
            return redirect(url_for('create_user'))
    return render_template('create_user.html', form=form)


@app.route('/update_user/<string:_id>', methods=['POST', 'GET'])
@login_required
def update_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id))
        form = UpdateUserForm(request.form, role=user.role, status=user.status)
        if request.method == 'POST' and form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            login = form.login.data
            password_hash = generate_password_hash(form.password.data)
            role = form.role.data
            status = form.status.data
            user.update(firstname=firstname, lastname=lastname,
                        email=email, login=login, password_hash=password_hash,
                        role=role, status=status)

            flash('User successfully updated', 'success')
            return redirect(url_for('get_active_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_active_users_list'))
    return render_template('update_user.html', user=user, form=form)


@app.route('/delete_user/<string:_id>')
@login_required
def delete_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id), status='active')
        user.update(status='inactive')
        flash('User successfully deleted', 'danger')
        return redirect(url_for('get_active_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_active_users_list'))


@app.route('/restore_user/<string:_id>')
@login_required
def restore_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id), status='inactive')
        user.update(status='active')
        flash('User successfully restored', 'success')
        return redirect(url_for('get_active_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_active_users_list'))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = User.objects(login=form.admin.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/admin_login')
        if admin.role == 'admin':
            login_user(admin)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('start_page')
            return redirect(next_page)
    return render_template('admin_login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('start_page'))


@login.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


if __name__ == '__main__':
    app.run()
