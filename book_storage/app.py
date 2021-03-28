import os
import traceback

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, request, url_for
from forms import AddUserForm, UpdateUserForm
from mongoengine import connect
from werkzeug.security import generate_password_hash

from models import Users

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


@app.route('/active_users_list')
def get_active_users_list():
    users = Users.objects(status='active')
    return render_template('users_list.html', users=users)


@app.route('/inactive_users_list')
def get_inactive_users_list():
    users = Users.objects(status='inactive')
    return render_template('users_list.html', users=users)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = AddUserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = Users(email=form.email.data)
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.password = generate_password_hash(form.password.data, method='sha256')
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
def update_user(_id: str):
    try:
        user = Users.objects.get(id=ObjectId(_id))
        form = UpdateUserForm(request.form, role=user.role, status=user.status)
        if request.method == 'POST' and form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = generate_password_hash(form.password.data, method='sha256')
            role = form.role.data
            status = form.status.data
            user.update(firstname=firstname, lastname=lastname,
                        email=email, password=password,
                        role=role, status=status)

            flash('User successfully updated', 'success')
            return redirect(url_for('get_active_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_active_users_list'))
    return render_template('update_user.html', user=user, form=form)


@app.route('/delete_user/<string:_id>')
def delete_user(_id: str):
    try:
        user = Users.objects.get(id=ObjectId(_id), status='active')
        user.update(status='inactive')
        flash('User successfully deleted', 'danger')
        return redirect(url_for('get_active_users_list'))
    except Exception as e:
        print('Something went wrong!')
        traceback.print_exc()
        return redirect(url_for('get_active_users_list'))


if __name__ == '__main__':
    app.run()
