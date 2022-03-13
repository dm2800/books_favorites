from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import book 


class Author:
    db = 'books_schema'
    def __init__(self,data):
        self.id = data['id']
        self.name= data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # NOW WE CREATE A LIST SO THAT LATER WE CAN ADD IN ALL THE BOOK OBJECTS THAT RELATE TO AN AUTHOR. 
        self.favorites = [] # THIS IS WHERE WE'LL APPEND BOOK FAVORITES FARTHER DOWN. 

    @classmethod
    # gets all the authors and returns them in a list of author objects.
    def get_all(cls):
        query = "SELECT * FROM authors;"
        authors_from_db =  connectToMySQL(cls.db).query_db(query)
        authors =[]
        for row in authors_from_db:
            authors.append(cls(row))
        return authors

    @classmethod
    def save(cls,data):
        query = "INSERT INTO authors (name,created_at,updated_at) VALUES (%(name)s,NOW(),NOW())"
        return connectToMySQL(cls.db).query_db(query,data)


    #THE FOLLOWING METHOD WILL RETRIEVE THE author WITH ALL THE BOOKS THAT ARE ASSOCIATED WITH THE AUTHOR. 
    @classmethod
    def get_one_with_favorites( cls, data ):
        #  need favorites to act as a BRIDGE for the many to many relationship, to relate the book to the author.
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db( query, data)
        #RESULTS WILL BE A LIST OF FAVORITE OBJECTS WITH THE AUTHOR ATTACHED TO EACH ROW. 
        author = cls(results[0])
        for row in results: 
            #if there are no favorites
            if row['books.id'] == None:
                break 

            book_data = {
                "id" : row["books.id"],
                "title" : row["title"],
                "num_of_pages" : row["num_of_pages"],
                "created_at" : row["books.created_at"],
                "updated_at" : row["books.updated_at"],
            }
            author.favorites.append ( book.Book ( book_data ))
        return author 

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM authors WHERE authors.id = %(id)s;"
        author_from_db = connectToMySQL(cls.db).query_db(query,data)

        return cls(author_from_db[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE authors SET name=%(name)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM authors WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def add_fave(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def unfavorited_authors(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s );"
        authors = [] 
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            authors.append(cls(row))
        return authors 
