import os
import traceback

from bson import ObjectId
from dotenv import load_dotenv
from flask import flash, Flask, redirect, render_template, request, url_for
from forms import AddUserForm, UpdateUserForm
from mongoengine import connect
from werkzeug.security import generate_password_hash

from models import User

load_dotenv()

connect(
    db=os.getenv('DB_NAME'),
    host=os.getenv('MONGO_URL'),
    port=int(os.getenv('PORT'))
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def start_page():
    return render_template('index.html')


@app.route('/users_list')
def get_users_list():
    users = User.objects.order_by('email', 'status')
    return render_template('users_list.html', users=users)


@app.route('/active_users_list')
def get_active_users_list():
    users = User.objects(status='active').order_by('email', 'status')
    return render_template('users_list.html', users=users)


@app.route('/inactive_users_list')
def get_inactive_users_list():
    users = User.objects(status='inactive').order_by('email', 'status')
    return render_template('users_list.html', users=users)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = AddUserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = User(email=form.email.data)
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.login = form.login.data
            user.password = generate_password_hash(form.password.data, method='sha256')
            user.role = form.role.data
            user.status = 'active'
            user.save()
            flash('User successfully created', 'success')
            return redirect(url_for('get_users_list'))
        except Exception as e:
            print("Something went wrong!")
            traceback.print_exc()
            return redirect(url_for('create_user'))
    return render_template('create_user.html', form=form)


@app.route('/update_user/<string:_id>', methods=['POST', 'GET'])
def update_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id))
        form = UpdateUserForm(request.form, role=user.role, status=user.status)
        if request.method == 'POST' and form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            login = form.login.data
            password = generate_password_hash(form.password.data, method='sha256')
            role = form.role.data
            status = form.status.data
            user.update(firstname=firstname, lastname=lastname,
                        email=email, login=login, password=password,
                        role=role, status=status)

            flash('User successfully updated', 'success')
            return redirect(url_for('get_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_users_list'))
    return render_template('update_user.html', user=user, form=form)


@app.route('/delete_user/<string:_id>')
def delete_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id), status='active')
        user.update(status='inactive')
        flash('User successfully deleted', 'danger')
        return redirect(url_for('get_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_users_list'))


@app.route('/restore_user/<string:_id>')
def restore_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id), status='inactive')
        user.update(status='active')
        flash('User successfully restored', 'success')
        return redirect(url_for('get_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_users_list'))


if __name__ == '__main__':
    app.run()
