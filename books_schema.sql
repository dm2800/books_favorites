


SELECT * FROM books 
LEFT JOIN favorites ON favorites.book_id = books.id -- need favorites to act as a BRIDGE for the many to many relationship, to relate the book to the author. 
LEFT JOIN authors ON favorites.author_id = authors.id;


SELECT * FROM authors;

INSERT INTO authors (name) 
VALUES ('JK Rowling');

SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id;

SELECT * FROM authors LEFT JOIN favorites on favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id;

SELECT * FROM books LEFT JOIN authors ON authors.book_id = books.id;

INSERT INTO favorites (author_id, book_id)
VALUES (1, 1), (1, 2), (1,3), (1,4);

INSERT INTO favorites (author_id, book_id)
VALUES (2, 3), (2, 4), (2,5);


SELECT * FROM books;

SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = 1);


DELETE FROM favorites WHERE author_id = 7 AND author_id = 8 AND author_id = 9;


SELECT * FROM authors;

SELECT * FROM favorites; 



