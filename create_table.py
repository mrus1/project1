import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    # Create users table
    db.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    print(f"Table users created!")

    # Create books table
    db.execute("CREATE TABLE IF NOT EXISTS books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR, author VARCHAR, year VARCHAR)")
    print(f"Table books created!")
    db.commit()

    # Create reviews table
    db.execute("CREATE TABLE IF NOT EXISTS reviews (id SERIAL PRIMARY KEY, book_id INTEGER REFERENCES books, user_id INTEGER REFERENCES users, review VARCHAR, rating INTEGER)")
    print(f"Table reviews created!")

    db.commit()

if __name__ == "__main__":
    main()
