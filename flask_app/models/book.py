from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author 

class Book: 
    db = 'books_schema'
    def __init__( self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.num_of_pages = db_data['num_of_pages']
        # We need to have a list in case we want to show which authors are related to the favorite. 

        self.favorites = []
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save( cls, data ):
        query = "INSERT INTO books (title, num_of_pages, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

        #This method will retrieve the specific book along with all the authors who favorited  it. 
    @classmethod
    def get_book_with_authors(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        # RESULTS WILL BE A LIST OF Book OBJECTS WITH THE Author ATTACHED TO EACH ROW. 
        print (f'printing book results: {results}')
        book = cls(results[0])
        for row_from_db in results: 
            author_data = {
                "id" : row_from_db["authors.id"],
                "name" : row_from_db["name"],
                "created_at" : row_from_db["authors.created_at"], 
                "updated_at" : row_from_db["authors.updated_at"]
            }
            book.favorites.append( author.Author( author_data ) )
        return book 

    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s );"
        results = connectToMySQL(cls.db).query_db(query,data)
        books = []
        for row in results:
            books.append(cls(row))
        print(books)
        return books 

    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        books_from_db =  connectToMySQL(cls.db).query_db(query)
        books =[]
        print(f'printing {books}')
        for b in books_from_db:
            books.append(cls(b))
            print(f'printing {books}')
        return books

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM books WHERE books.id = %(id)s;"
        book_from_db = connectToMySQL(cls.db).query_db(query,data)

        return cls(book_from_db[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE books SET title=%(title)s, num_of_pages=%(num_of_pages)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

