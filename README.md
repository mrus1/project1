# Project 1

Web Programming with Python and JavaScript


## Overview

With Look4Book web application you as a user, are able to register, login/logout and search books from local database, give them a review, see reviews from other users and delete your reviews.


### Download, install and try app

1. Make sure you have installed python 3.6 or higher on a computer.
2. Install pip.
3. Download project to your computer.
4. In command line, navigate to downloaded folder and run "pip3 install -r requirements.txt"
5. Create Database and then run create_table.py file to create all needed tables for application. Then run import.py file, to import books into database from books.csv, so you will be able to test functionality of webapp.
6. Set the environment variables FLASK_APP=application.py, DATABASE_URL="url-of-your-database" (example on linux terminal: "export FLASK_APP=application.py")
7. Now you should be able to run and test application with "flask run" command from project directory.


## Project Root directory

#### requirements.txt
  Contains required Python packages to use applcation.

#### books.csv
  List of 5000 books with basic information.

#### create_table.py
  Contains queries for creating users, books, reviews tables in postgresql database.

#### import.py
  Contains query to import list of books from books.csv in books table of database.

#### application.py
  Checks for environment variable, configure session to use filesystem, set up database, routes, custom methods.

  Routes:

    "/" - check if user is logged in (session is set up)
      if true, get users data and render search bar, so user is able to search
      for books.
      If user submit search string from search form, custom search() method
      runs, and checks if there are any results for specific search string and
      shows them or return message that it can't find any books.
      else: make random search for books in database and show them on
      front page.

    "/login" - renders template login.html, where the login and register
      forms are.

    "/log_in" - if requested method on login page from log in form is "POST":
      check in database if submitted username and password exist, and if true,
      return index.html template.
      else: show error to user, that either username or password are not
      matching with any in database. return login.html template again,
      so user can try again.

    "/register" - if requested method on login page from register
      form is "POST": check in database if submitted username already exist
      and return error if true and login.html page, so user can try again.
      else: create new user in database and return login.html page, so user
      can now log in.

    "/log_out" - runs just when user is logged in and clicks on "logout" button.
      clear session and returns index.html template.

    "/book/<int:book_id>" - It shows up when user hit the "More" button
      from "/" route and contains all book informations (title, author,
      isbn, year) and reviews of users if there are any.
      Here is user also able to create or delete review for given book.

    "/delete/<int:review_id>/<int:book_id>" - if user hits the "delete"
      button, it executes delete query and removes review from current
      user from database.
      After that user is still on book information page,
      but its review is removed.

    "/api/<isbn>" - if you replace <isbn> with existing book isbn number,
    and if this book exists in local database, informations of wanted book
    are returned as a json object with title, author, isbn, year,
    review_count and average_score.

### /templates

#### layout.html
  It contains the whole layout of web application.
  Link tags for importing bootstrap, jinja2 "blocks" for title, navigation bar,
  login section in navigation bar which shows different buttons if user is
  logged in or not, heading block and body block.

#### index.html
  Below navigation bar, first thing is title of web application - Look4Book.
  Then there are two options. First: if the user is not logged in,
  then content of the page is random generated books from database.
  It is used card component from bootstrap. Second: if user is logged in,
  then on top is search bar/input form, and if search is successful,
  below shows up the results - bootstrap cards with book title,
  author and more button.

#### book.html
  First section is for information about book. For faster design
  I used bootstrap component - card. It shows book title, author, year,
  isbn number and back button.
  Next section is "Add review form", it contains textarea for
  comment about book, select tag for selecting book rating and submit button.
  Last section shows all submitted reviews if there are any.
  Again it is bootstrap card component with showing author of review,
  comment, rating and delete button for your own reviews.

#### login.html
  There are two sections, both are designed with bootstrap component jumbotron.
  First: Login form - username and password input field and submit button.
  Second: Registration form - username and password input field
  and submit button. Both has also "<small>" html tags to display
  error text if there is some when submitting forms.
  If there is no error after registration the h3 element
  is created with successful text,
  so user knows that it was successfully created.

### /static

#### style.scss
  Body: background color is set to #c9a53e
  .login: adds some space between login forms
  .error: styles error message below forms
  input: my custom styles for search bar
  media: changes width of container element for different screen sizes.
