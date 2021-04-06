import json
import os

from bson import ObjectId
from dotenv import load_dotenv
from flask import flash, Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required,  login_user, logout_user
from mongoengine import connect
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename


from forms import AddBookForm, AddUserForm, LoginForm, UpdateBookForm, UpdateUserForm
from models import Book, Status, User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

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


@app.route('/users_list')
def get_users_list():
    users = User.objects.order_by('email', 'status')
    return render_template('users_list.html', users=users)


@app.route('/active_users_list')
@login_required
def get_active_users_list():
    users = User.objects(status=Status.ACTIVE).order_by('email', 'status')
    return render_template('users_list.html', users=users)


@app.route('/inactive_users_list')
@login_required
def get_inactive_users_list():
    users = User.objects(status=Status.INACTIVE).order_by('email', 'status')
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
            user.status = Status.ACTIVE
            user.save()
            flash('User successfully created', 'success')
            return redirect(url_for('get_users_list'))
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect(url_for('create_user'))
    return render_template('create_user.html', form=form)


@app.route('/update_user/<string:_id>', methods=['POST', 'GET'])
@login_required
def update_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id))
        form = UpdateUserForm(
            request.form, firstname=user.firstname, lastname=user.lastname,
            email=user.email, login=user.login, role=user.role, status=user.status)
        form.user_id.data = user.id
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
            return redirect(url_for('get_users_list'))
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect(url_for('get_users_list'))
    return render_template('update_user.html', user=user, form=form)


@app.route('/delete_user/<string:_id>')
@login_required
def delete_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id), status='active')
        user.update(status='inactive')
        flash('User successfully deleted', 'danger')
        return redirect(url_for('get_users_list'))
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect(url_for('get_users_list'))


@app.route('/restore_user/<string:_id>')
@login_required
def restore_user(_id: str):
    try:
        user = User.objects.get(id=ObjectId(_id), status='inactive')
        user.update(status='active')
        flash('User successfully restored', 'success')
        return redirect(url_for('get_users_list'))
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect(url_for('get_users_list'))


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


@app.route('/add-book', methods=['POST', 'GET'])
@login_required
def add_book():
    form = AddBookForm(request.form)
    if request.method == 'POST':
        book = Book()
        book.title = form.title.data
        book.author = form.author.data
        book.year = form.year.data
        book.publisher = form.publisher.data
        book.language = form.language.data
        book.description = form.description.data
        book.pages = form.pages.data
        book.genres = form.genre.data
        book.status = Status.ACTIVE
        try:
            book.save()
            return redirect('/book-storage')
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect('/add-book')
    return render_template('add-book.html', form=form)

@app.route('/import-file')
@login_required
def import_file():
    return render_template('csv-import.html')


@app.route('/import-file', methods=['POST', 'GET'])
@login_required
def uploadFiles():
    if request.method == 'POST' and request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            flash('File has not been selected, please choose one.', 'warning')
            return redirect(request.url)
        if not (uploaded_file.filename.endswith('.json')):
            flash('Incorrect type of file (.JSON is needed)', 'danger')
            return redirect(request.url)
        else:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)
        try:
            with open(os.getenv('UPLOAD_FOLDER') + filename) as f:
                file_data = json.load(f)
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(request.url)
        finally:
            os.remove(file_path)
        try:
            for example in file_data:
                book = Book.from_json(json.dumps(example))
                book.save(force_insert=True)
            flash('Books added successfully', 'success')
            return redirect(url_for('import_file'))
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('import_file'))


@app.route('/book-storage')
@login_required
def book_storage():
    books = Book.objects()
    return render_template('book-storage.html', books=books)

@app.route('/book-active')
@login_required
def book_active():
    books = Book.objects(status=Status.ACTIVE)
    return render_template('book-active.html', books=books)


@app.route('/book-inactive')
@login_required
def book_inactive():
    books = Book.objects(status=Status.INACTIVE)
    return render_template('book-inactive.html', books=books)


@app.route('/book-storage/<string:_id>')
@login_required
def book_details(_id):
    book = Book.objects.get(id=ObjectId(_id))
    return render_template('book-details.html', book=book)


@app.route('/book-update/<string:_id>', methods=['POST', 'GET'])
@login_required
def book_update(_id):
    try:
        book = Book.objects.get(id=ObjectId(_id))
        form = UpdateBookForm(request.form)
        if request.method == 'POST':
            title = form.title.data
            author = form.author.data
            year = form.year.data
            publisher = form.publisher.data
            language = form.language.data
            description = form.description.data
            pages = form.pages.data
            genres = form.genre.data
            status = form.status.data
            book.update(title=title, author=author, year=year, publisher=publisher, language=language,
                        description=description, pages=pages, genres=genres, status=status)
            return redirect('/book-storage')
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect('/home')
    return render_template('update-book.html', book=book, form=form)


@app.route('/book-delete/<string:_id>')
@login_required
def book_delete(_id):
    try:
        book = Book.objects.get(id=ObjectId(_id), status=Status.ACTIVE)
        book.update(status=Status.INACTIVE)
        return redirect('/book-active')
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect('/home')


@app.route('/book-restore/<string:_id>')
@login_required
def book_restore(_id):
    try:
        book = Book.objects.get(id=ObjectId(_id), status=Status.INACTIVE)
        book.update(status=Status.ACTIVE)
        return redirect('/book-inactive')
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect('/home')


if __name__ == '__main__':
    app.run()
