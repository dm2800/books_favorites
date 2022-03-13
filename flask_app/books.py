from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.book import Book
from flask_app.models.author import Author



@app.route('/')
def bindex(): 
	return render_template('books.html',books=Book.get_all())

@app.route('/books/')
def books():
	return render_template('books.html',books=Book.get_all())
        

@app.route('/books/create/',methods=['POST'])
def create_book():
	data = {
			"title" : request.form["title"],
			"num_of_pages" : request.form["num_of_pages"]
	}
	Book.save(data)
	return redirect('/books/')
        
@app.route('/books/<int:id>/') 
def view_book(id):
	data = {
		'id': id
	}
	return render_template('viewbook.html', book=Book.get_book_with_authors(data), unfavorited_authors = Author.unfavorited_authors(data))


@app.route('/addfaveauthor/', methods=['POST'])
def add_fave_author():
	data = {
		'author_id': request.form['author_id'],
		'book_id': request.form['book_id']
	}
	Author.add_fave(data)
	return redirect (f"/books/{request.form['book_id']}")