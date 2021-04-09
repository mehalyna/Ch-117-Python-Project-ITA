import json
import os

from bson import ObjectId
from datetime import timedelta
from dotenv import load_dotenv
from flask import flash, Flask, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

from forms import AddBookForm, AddUserForm, LoginForm, UpdateBookForm, UpdateUserForm
from models import Author, Book, Statistics, Status, User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=90)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 Mb limit

connect(
    db=os.getenv('DB_NAME'),
    host=os.getenv('MONGO_URL'),
    port=int(os.getenv('PORT'))
)

login = LoginManager(app)
login.login_view = 'admin_login'
login.init_app(app)

ROWS_PER_PAGE = 6


@app.route('/')
@login_required
def start_page():
    num_users = User.objects.count()
    num_books = Book.objects.count()
    num_active_users = User.objects(status=Status.ACTIVE).count()
    num_inactive_users = User.objects(status=Status.INACTIVE).count()
    num_muted_users = User.objects(status=Status.MUTED).count()
    num_active_books = Book.objects(status=Status.ACTIVE).count()
    num_inactive_books = Book.objects(status=Status.INACTIVE).count()

    statistics = Statistics(num_users, num_books, num_active_users, num_inactive_users, num_muted_users,
                            num_active_books, num_inactive_books)

    return render_template('index.html', statistics=statistics)


@app.route('/users_list')
def get_users_list():
    search = request.args.get('userSearch')
    page = request.args.get('page', 1, type=int)
    if search:
        users = User.objects(
            Q(firstname__contains=search) | Q(lastname__contains=search) | Q(email__contains=search),
            status=Status.ACTIVE).order_by('email', 'status').paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        users = User.objects(status=Status.ACTIVE).order_by('email', 'status').paginate(page=page,
                                                                                        per_page=ROWS_PER_PAGE)
    return render_template('users_list.html', users=users)


@app.route('/active_users_list')
@login_required
def get_active_users_list():
    page = request.args.get('page', 1, type=int)
    users = User.objects(status=Status.ACTIVE).order_by('email', 'status').paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('users_list.html', users=users)


@app.route('/inactive_users_list')
@login_required
def get_inactive_users_list():
    page = request.args.get('page', 1, type=int)
    users = User.objects(status=Status.INACTIVE).order_by('email', 'status').paginate(page=page, per_page=ROWS_PER_PAGE)
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
        if admin is None or not admin.check_password(form.password.data) or admin.status != 'active':
            flash('Invalid username or password')
            return redirect('/admin_login')
        if admin.role == 'admin':
            login_user(admin)
            session.permanent = True
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('start_page')
            return redirect(next_page)
    return render_template('admin_login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin_login'))


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
        author_name = form.author_name.data
        author_birthdate = str(form.author_birthdate.data)
        author_death_date = str(form.author_death_date.data)
        book.year = form.year.data
        book.publisher = form.publisher.data
        book.language = form.language.data
        book.description = form.description.data
        book.pages = form.pages.data
        book.genres = [form.genre.data]
        book.save()

        try:
            author = Author.objects(name=author_name, birthdate=author_birthdate, death_date=author_death_date).first()
            if author and not str(book.pk) in author.books:
                author.books.append(str(book.pk))

            if not author:
                author = Author(name=author_name, birthdate=author_birthdate, death_date=author_death_date,
                                books=[str(book.id)])

            author.save()
            book.author_id = author.pk
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
def upload_files():
    if request.method == 'POST' and request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            flash('File has not been selected, please choose one.', 'warning')
            return redirect(request.url)
        if not (uploaded_file.filename.endswith('.json')):
            flash('Incorrect type of file (.JSON is needed)', 'danger')
            return redirect(request.url)
        try:
            data = json.loads(uploaded_file.read().decode())
        except Exception as e:
            flash(f'Error parsing file: {str(e)}', 'danger')
            print(e)
            return redirect(request.url)

        try:
            books = []
            for row in data:
                author = Author.objects(**row['author']).first()
                if author:
                    row.pop('author')
                    books.append(Book(author_id=author.pk, **row))
                else:
                    author = Author(**row['author'])
                    author.save()
                    row.pop('author')
                    books.append(Book(author_id=author.pk, **row))

            Book.objects.insert(books)
            for book in books:
                book.author_id.books.append(str(book.id))
                book.cascade_save()
        except Exception as e:
            flash(f'Error saving object: {str(e)}', 'danger')
            return redirect(url_for('import_file'))

        flash('All books saved successfully', 'success')
        return redirect(url_for('import_file'))


@app.route('/book-storage')
@login_required
def book_storage():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('bookSearch')
    if search:
        books = Book.objects(Q(title__contains=search) | Q(year__contains=search)).paginate(page=page, per_page=ROWS_PER_PAGE)
        author = Author.objects(name__contains=search).first()
        if author:
            arr = []
            for i in author.books:
                arr.append(Book.objects(id=i).first())
            books.items += arr
    else:
        books = Book.objects.order_by('title', 'status').paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('book-storage.html', books=books)


@app.route('/book-active')
@login_required
def book_active():
    page = request.args.get('page', 1, type=int)
    books = Book.objects(status=Status.ACTIVE).order_by('title', 'status').paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('book-storage.html', books=books)


@app.route('/book-inactive')
@login_required
def book_inactive():
    page = request.args.get('page', 1, type=int)
    books = Book.objects(status=Status.INACTIVE).order_by('title', 'status').paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('book-storage.html', books=books)


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
            author_name = form.author_name.data
            author_birthdate = str(form.author_birthdate.data)
            author_death_date = str(form.author_death_date.data)
            year = form.year.data
            publisher = form.publisher.data
            language = form.language.data
            description = form.description.data
            pages = form.pages.data
            genres = form.genre.data
            status = form.status.data
            if str(book.id) in book.author_id.books:
                book.author_id.books.remove(str(book.id))
                book.cascade_save()
            # take only first author
            author = Author.objects(name=author_name, birthdate=author_birthdate, death_date=author_death_date).first()
            if author and not str(book.id) in author.books:
                author.books.append(str(book.id))
            if not author:
                author = Author(name=author_name, birthdate=author_birthdate, death_date=author_death_date,
                                books=[str(book.id)])
            author.save()
            book.update(title=title, author_id=author.pk, year=year, publisher=publisher, language=language,
                        description=description, pages=pages, genres=[genres], status=status)
            return redirect('/book-storage')
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect('/book-storage')
    return render_template('update-book.html', book=book, form=form)


@app.route('/book-delete/<string:_id>')
@login_required
def book_delete(_id):
    try:
        book = Book.objects.get(id=ObjectId(_id), status=Status.ACTIVE)
        book.update(status=Status.INACTIVE)
        return redirect('/book-storage')
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect('/book-storage')


@app.route('/book-restore/<string:_id>')
@login_required
def book_restore(_id):
    try:
        book = Book.objects.get(id=ObjectId(_id), status=Status.INACTIVE)
        book.update(status=Status.ACTIVE)
        return redirect('/book-storage')
    except Exception as e:
        print(e)
        flash(str(e), 'danger')
        return redirect('/book-storage')


if __name__ == '__main__':
    app.run()
