
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.author import Author
from flask_app.models.book import Book



@app.route('/')
def aindex(): 
	return render_template('authors.html',authors=Author.get_all())

@app.route('/authors/')
def authors():
	return render_template('authors.html',authors=Author.get_all())
        


@app.route('/authors/create/',methods=['POST'])
def create_author():
	data = {
			"name" : request.form['name']
	}
	author_id = Author.save(data)
	return redirect('/authors/')
        

@app.route('/authors/<int:id>/')
def view_author(id):
	data = {
		'id': id
	}
	return render_template('viewauthor.html', author = Author.get_one_with_favorites(data), unfavorited_books=Book.unfavorited_books(data))
        

@app.route('/addfavebook/', methods=['POST'])
def add_fave_book():
	data = {
		'author_id': request.form['author_id'],
		'book_id': request.form['book_id']
	}
	Author.add_fave(data)
	return redirect (f"/authors/{request.form['author_id']}")



