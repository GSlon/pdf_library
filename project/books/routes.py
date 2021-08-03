import os
from flask import render_template, url_for, flash, redirect, Blueprint, current_app, send_file
from flask_login import current_user, login_required
from project import db
from project.models import Book
from project.books.forms import BookForm
from .tagger import get_tags
from .utils import save_book_file

books = Blueprint('books', __name__)


@books.route("/book/new", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        if form.pdfile.data:
            path = save_book_file(form.pdfile.data)
            tags = get_tags(form.pdfile.data)
            book = Book(title=form.title.data, author=form.author.data, path=path, tags=tags, user=current_user)
            db.session.add(book)
            db.session.commit()
        flash('Your book has been added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_book.html', title='New Book', form=form, legend='New Book')


@books.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)

    try:
        return send_file(os.path.join(current_app.root_path, 'static', book.path))
    except FileNotFoundError:
        return render_template('errors/404.html')



