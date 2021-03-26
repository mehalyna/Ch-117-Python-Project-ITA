import os

from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, request
from forms import AddUserForm, UpdateUserForm
from mongoengine import connect
from mongoengine.errors import NotUniqueError, DoesNotExist
from pymongo import MongoClient
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
    return render_template('base.html')


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
    if request.method == 'POST':
        try:
            user = Users(email=form.email.data)
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.password = generate_password_hash(form.password.data, method='sha256')
            user.role = form.role.data
            user.status = 'active'
            user.save()
        except NotUniqueError as e:
            print("E-mail already found")
        flash('User successfully created', 'success')
        return redirect('/active_users_list')
    return render_template('create_user.html', form=form)


@app.route('/update_user/<string:_id>', methods=['POST', 'GET'])
def update_user(_id):
    try:
        user = Users.objects.get(id=ObjectId(_id))
        form = UpdateUserForm(request.form, role=user.role, status=user.status)
        if request.method == 'POST':
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
            return redirect('/active_users_list')
    except (DoesNotExist, InvalidId) as e:
        print('Such user doesn\'t exist')
        print(e)
        return redirect('/active_users_list')
    return render_template('update_user.html', user=user, form=form)


@app.route('/delete_user/<string:_id>')
def delete_user(_id):
    try:
        user = Users.objects.get(id=ObjectId(_id), status='active')
        user.update(status='inactive')
        flash('User successfully deleted', 'danger')
        return redirect('/active_users_list')
    except (DoesNotExist, InvalidId) as e:
        print('User is already inactive or such user doesn\'t exist')
        return redirect('/active_users_list')


if __name__ == '__main__':
    app.run(debug=True)
