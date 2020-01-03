import os
import requests
import random

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# ROUTES

@app.route("/", methods=["GET", "POST"])
def index():
    error = False
    books = []
    # Session set up
    if session.get("user_id") is None:
        books = random_books()
        return render_template("index.html", books_random = books)
    else:
        user_data = get_user()
        if request.method == "POST":
            books = search()
            if not books:
                error = True
        return render_template("index.html", error = error, books = books, username = user_data["username"], user_id = user_data["user_id"])



@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/log_in", methods=["GET", "POST"])
def log_in():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if (user is None):
            error = 1
            return render_template("login.html", error = error )
        elif not check_password_hash(user["password"], password):
            error = 2
            return render_template("login.html", error = error )
        else:
            session.clear()
            session["user_id"] = user["id"]
            return index()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("userNew")
        password = request.form.get("passNew")
        error = None

        if not username:
            error = 1
            return render_template("login.html", error = error)
        elif not password:
            error = 2
            return render_template("login.html", error = error)
        elif db.execute("SELECT username FROM users WHERE username = :username", {"username": username}).fetchone() is not None:
            error = 3
            return render_template("login.html", error = error, username = username)

        if error is None:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": username, "password": generate_password_hash(password)})
            db.commit()

    return render_template("login.html", error = error, username = username)

@app.route("/log_out", methods=["GET"])
def log_out():
    session.clear()
    return index()

# Book information page
@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    if session.get("user_id") is None:
        books = random_books()
        return render_template("index.html", books_random = books)
    else:
        user_data = get_user()
        book_info = db.execute("SELECT title, author, isbn, year FROM books WHERE id = :book_id", {"book_id": book_id}).fetchall()[0]

        review_info = db.execute("SELECT username, review, rating, reviews.id FROM reviews, users WHERE book_id = :book_id AND users.id = reviews.user_id", {"book_id": book_id}).fetchall()

    # Create a comment
    if request.method == "POST":
        review = request.form.get("comment")
        rating = request.form.get("rating")
        if review.strip():
            post_review = db.execute("INSERT INTO reviews (book_id, user_id, review, rating) VALUES (:book_id, :user_id, :review, :rating)", {"book_id": book_id, "user_id": user_data["user_id"], "review": review, "rating": rating})
            db.commit()
            print("ATTENTION, NEW COMMENT WAS CREATED!")
            return redirect(url_for("book", book_id=book_id))


    return render_template("book.html", book_info = book_info, book_id = book_id, review_info = review_info, username = user_data["username"], user_id = user_data["user_id"])


@app.route("/delete/<int:review_id>/<int:book_id>", methods=["GET"])
def delete(review_id, book_id):
    review_id = review_id
    book_id = book_id

    delete_review = db.execute("DELETE FROM reviews WHERE id = :review_id", {"review_id": review_id})
    db.commit()
    print("COMMENT WAS SUCCESSFULY REMOVED")

    return redirect(url_for("book", book_id=book_id))

# API Access
@app.route("/api/<isbn>", methods=["GET"])
def book_api(isbn):
    # Get isbn value from url
    isbn_length = len(isbn)
    isbn = '{isbn:0>{isbn_length}}'.format(isbn = isbn, isbn_length = isbn_length)

    # Query for book
    book = db.execute("SELECT title, author, isbn, year, id FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()

    # If retreived list is empty
    if not book:
        return jsonify({"error": "Invalid isbn"}), 422

    book = book[0]
    book_id = book.id
    review_info = db.execute("SELECT COUNT(id), AVG(rating) FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchall()
    if review_info[0][0]:
        review_count = review_info[0][0]
    else:
        review_count = 0

    if review_info[0][1]:
        average_score = format(review_info[0][1], '.1f')
    else:
        average_score = 0

    db.commit()
    # Return book information as json object
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": review_count,
        "average_score": average_score
    })


# END ROUTES

if __name__ == "__main__":
    app.run()


# METHODS

# Get the user data
def get_user():
    user_id = session.get("user_id")
    username = db.execute("SELECT username FROM users WHERE id = :id",
        {"id": user_id}).fetchone().username
    return {"user_id": user_id, "username": username}

# Search for books
def search():

    search_string = request.form.get("search_string")

    if search_string:
        if search_string[0] in '0123456789':
            search_string = "%" + search_string.upper() + "%"
        else:
            search_string = "%" + search_string.lower() + "%"
        print(f"Your search string is: " + search_string)
        books = db.execute(
                """SELECT title, author, id FROM books WHERE isbn LIKE :search_string
                OR LOWER (title) LIKE :search_string OR LOWER (author) LIKE
                :search_string OR year LIKE :search_string LIMIT 6""",
                {"search_string": search_string}
                ).fetchall()
        db.commit()
        print(books)
        return (books)

print("No results!")



# Generate random books for preview
def random_books():
    book_ids = []
    for i in range(3):
        i = random.randrange(1, 5000)
        book_ids.append(i)
    books = db.execute(
        """SELECT title, author FROM books WHERE id in (:id_1, :id_2, :id_3)""",
        {"id_1": book_ids[0], "id_2": book_ids[1], "id_3": book_ids[2]}
    ).fetchall()
    db.commit()
    return books
