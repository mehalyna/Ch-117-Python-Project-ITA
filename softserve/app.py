from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/softserve"
mongo = PyMongo(app)
books_collection = mongo.db.book


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/books-storage')
def books_storage():
    books = books_collection.find({})
    return render_template('books-storage.html', books=books)


@app.route('/books-storage/<string:_id>')
def books_storage_details(_id):
    book = books_collection.find_one({'_id': ObjectId(_id)})
    return render_template('books-storage-details.html', book=book)


@app.route('/books-storage/<string:_id>/del')
def books_storage_del(_id):
    book = books_collection.find_one({'_id': ObjectId(_id)})
    try:
        books_collection.delete_one(book)
        return redirect('/books-storage')
    except:
        return 'There was mistake during deletion'


@app.route('/books-storage/<string:_id>/update', methods=['POST', 'GET'])
def books_storage_update(_id):
    book = books_collection.find_one({'_id': ObjectId(_id)})
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        publisher = request.form['publisher']
        number_of_pages = request.form['number_of_pages']
        description = request.form['description']
        language = request.form['language']

        try:
            books_collection.update(book, {'title': title, 'author': author, 'genre': genre, 'year': year,
                                           'language': language, 'publisher': publisher,
                                           'number_of_pages': number_of_pages, 'description': description})
            return redirect('/books-storage')
        except:
            return 'There was mistake during updating'

    else:
        return render_template('books-storage-update.html', book=book)


@app.route('/add-book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        publisher = request.form['publisher']
        number_of_pages = request.form['number_of_pages']
        description = request.form['description']
        language = request.form['language']

        try:
            books_collection.insert_one({'title': title, 'author': author, 'genre': genre, 'year': year,
                                           'language': language, 'publisher': publisher,
                                           'number_of_pages': number_of_pages, 'description': description})
            return redirect('/books-storage')
        except:
            return 'There was a mistake'

    else:
        return render_template('add-book.html')


if __name__ == "__main__":
    app.run(debug=True)
