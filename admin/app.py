import json
import os
import re

from bson import ObjectId
from datetime import timedelta
from dotenv import load_dotenv
from flask import flash, Flask, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from mongoengine import connect
from urllib import parse
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

from admin.forms import AddBookForm, AddUserForm, LoginForm, UpdateBookForm, UpdateUserForm
from admin.models import Author, Book, Role, Statistics, Status, User
import admin.utils as utils


load_dotenv()


def create_app():
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

    @app.errorhandler(404)
    def page_not_found(e):
        prev_url = request.referrer
        query = parse.parse_qs(parse.urlparse(prev_url).query)
        page = query.get('page')
        user_search = query.get('userSearch')
        book_search = query.get('bookSearch')

        if page and page[0].isdigit() or user_search or book_search:
            url_to_redirect = prev_url.split('?')[0] + '?'
            if page:
                page_value = int(page[0]) - 1
                url_to_redirect += f'&{"page"}={page_value}'
            if user_search:
                user_search_value = user_search[0]
                url_to_redirect += f'&{"userSearch"}={user_search_value}'
            if book_search:
                book_search_value = book_search[0]
                url_to_redirect += f'&{"bookSearch"}={book_search_value}'

            return redirect(url_to_redirect)

        return 'Page not found'

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
    @login_required
    def get_users_list():
        users = utils.search_and_pagination(collection=User, order_field='email')
        return render_template('users_list.html', users=users)

    @app.route('/active_users_list')
    @login_required
    def get_active_users_list():
        users = utils.search_and_pagination(collection=User, order_field='email', status=Status.ACTIVE)
        return render_template('users_list.html', users=users)

    @app.route('/inactive_users_list')
    @login_required
    def get_inactive_users_list():
        users = utils.search_and_pagination(collection=User, order_field='email', status=Status.INACTIVE)
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
                if _id == session.get('_user_id') and (status != Status.ACTIVE or role != Role.ADMIN):
                    flash('The administrator cannot change the status or role for himself', 'warning')
                else:
                    user.update(firstname=firstname, lastname=lastname,
                                email=email, login=login, password_hash=password_hash,
                                role=role, status=status)
                    flash('User successfully updated', 'success')
                return redirect(utils.back_to_page('page', 'userSearch', 'urlPath'))
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect(utils.back_to_page('page', 'userSearch', 'urlPath'))
        return render_template('update_user.html', user=user, form=form)

    @app.route('/delete_user/<string:_id>')
    @login_required
    def delete_user(_id: str):
        try:
            user = User.objects.get(id=ObjectId(_id), status=Status.ACTIVE)
            if _id == session.get('_user_id'):
                flash('The administrator cannot change the status or role for himself', 'warning')
            else:
                user.update(status=Status.INACTIVE)
                flash('User successfully deleted', 'danger')
            return redirect(utils.back_to_page('page', 'userSearch', 'urlPath'))
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect(utils.back_to_page('page', 'userSearch', 'urlPath'))

    @app.route('/restore_user/<string:_id>')
    @login_required
    def restore_user(_id: str):
        try:
            user = User.objects.get(id=ObjectId(_id), status=Status.INACTIVE)
            user.update(status='active')
            flash('User successfully restored', 'success')
            return redirect(utils.back_to_page('page', 'userSearch', 'urlPath'))
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect(utils.back_to_page('page', 'userSearch', 'urlPath'))

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
            book.link_img = form.img_link.data
            book.publisher = form.publisher.data
            book.language = form.language.data
            book.description = form.description.data
            book.pages = form.pages.data
            book.genres = re.split(r',', form.genre.data)

            try:
                book.save()
                author = Author.objects(name=author_name, birthdate=author_birthdate,
                                        death_date=author_death_date).first()
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
        books = utils.search_and_pagination(collection=Book, order_field='title')
        return render_template('book-storage.html', books=books)

    @app.route('/book-active')
    @login_required
    def book_active():
        books = utils.search_and_pagination(collection=Book, order_field='title', status=Status.ACTIVE)
        return render_template('book-storage.html', books=books)

    @app.route('/book-inactive')
    @login_required
    def book_inactive():
        books = utils.search_and_pagination(collection=Book, order_field='title', status=Status.INACTIVE)
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
                book.link_img = form.img_link.data
                publisher = form.publisher.data
                language = form.language.data
                description = form.description.data
                pages = form.pages.data
                genres = re.split(r',', form.genre.data)
                status = form.status.data
                if str(book.id) in book.author_id.books:
                    book.author_id.books.remove(str(book.id))
                    book.cascade_save()
                # take only first author
                author = Author.objects(name=author_name, birthdate=author_birthdate,
                                        death_date=author_death_date).first()
                if author and not str(book.id) in author.books:
                    author.books.append(str(book.id))
                if not author:
                    author = Author(name=author_name, birthdate=author_birthdate, death_date=author_death_date,
                                    books=[str(book.id)])
                author.save()
                book.update(title=title, author_id=author.pk, year=year, publisher=publisher, language=language,
                            description=description, pages=pages, genres=genres, status=status)
                return redirect(utils.back_to_page('page', 'bookSearch', 'urlPath'))
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect(utils.back_to_page('page', 'bookSearch', 'urlPath'))
        return render_template('update-book.html', book=book, form=form)

    @app.route('/book-delete/<string:_id>')
    @login_required
    def book_delete(_id):
        try:
            book = Book.objects.get(id=ObjectId(_id), status=Status.ACTIVE)
            book.update(status=Status.INACTIVE)
            return redirect(utils.back_to_page('page', 'bookSearch', 'urlPath'))
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect(utils.back_to_page('page', 'bookSearch', 'urlPath'))

    @app.route('/book-restore/<string:_id>')
    @login_required
    def book_restore(_id):
        try:
            book = Book.objects.get(id=ObjectId(_id), status=Status.INACTIVE)
            book.update(status=Status.ACTIVE)
            return redirect(utils.back_to_page('page', 'bookSearch', 'urlPath'))
        except Exception as e:
            print(e)
            flash(str(e), 'danger')
            return redirect(utils.back_to_page('page', 'bookSearch', 'urlPath'))

    return app


if __name__ == '__main__':
    create_app().run()
