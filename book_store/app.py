from flask import Flask, render_template, flash, redirect
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, logout_user, login_user, login_required
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
login = LoginManager(app)
login.login_view = 'admin_login'
login.init_app(app)

from forms import LoginForm
from models import Admin

csrf = CSRFProtect(app)


@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='index')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.objects(username=form.admin.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/admin_login')
        login_user(admin)
        return redirect('/index')
    return render_template('admin_login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


if __name__ == '__main__':
    app.run()
