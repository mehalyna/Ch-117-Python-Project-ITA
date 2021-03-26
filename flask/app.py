from bson import ObjectId
from flask import Flask, render_template, flash, redirect, request
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from forms import AddUserForm, UpdateUserForm

client = MongoClient('localhost', 27017)
db = client['projectITA']
users_col = db['users']
app = Flask(__name__)
SECRET_KEY = "TEST"
app.config["SECRET_KEY"] = SECRET_KEY


@app.route('/')
def start_page():
    return render_template('base.html')


@app.route('/active_users_list')
def get_active_users_list():
    users_list = users_col.find({'status': 'active'})
    return render_template('users_list.html', user_list=users_list)


@app.route('/inactive_users_list')
def get_inactive_users_list():
    inactive_users_list = users_col.find({'status': 'inactive'})
    return render_template('users_list.html', user_list=inactive_users_list)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = AddUserForm(request.form)
    if request.method == 'POST':
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='sha256')
        role = form.role.data
        users_col.insert_one({'firstname': firstname, 'lastname': lastname,
                              'email': email, 'password': password,
                              'role': role, 'status': 'active'})
        flash('User successfully created', 'success')
        return redirect('/active_users_list')
    return render_template('create_user.html', form=form)


@app.route('/update_user/<string:_id>', methods=['POST', 'GET'])
def update_user(_id):
    user = users_col.find_one({'_id': ObjectId(_id)})
    form = UpdateUserForm(request.form, role=user['role'], status=user['status'])
    if request.method == 'POST':
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='sha256')
        role = form.role.data
        status = form.status.data
        users_col.update_one(
            {'_id': ObjectId(_id)}, {'$set': {
                'firstname': firstname, 'lastname': lastname,
                'email': email, 'password': password,
                'role': role, 'status': status
            }})
        flash('User successfully updated', 'success')
        return redirect('/active_users_list')
    return render_template('update_user.html', user=user, form=form)


@app.route('/delete/<string:_id>')
def delete_user(_id):
    status = 'inactive'
    users_col.update_one({'_id': ObjectId(_id)},
                         {'$set': {'status': status}})
    flash('User successfully deleted', 'danger')
    return redirect('/active_users_list')


if __name__ == '__main__':
    app.run(debug=True)
