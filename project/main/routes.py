from flask import render_template, request, Blueprint, redirect, url_for
from project.models import Book
from sqlalchemy import or_

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	books = Book.query.order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', books=books)


@main.route('/search/', methods=['GET'])
def search():
	page = request.args.get('page', 1, type=int)
	query = request.args.get('q')
	if not query:
		return redirect(url_for('main.home'))
	books = Book.query.filter(or_(
		Book.title.contains(query), 
		Book.author.contains(query),
		Book.tags.contains(query))).paginate(page=page, per_page=5)
	return render_template('search.html', books=books, query=query)
