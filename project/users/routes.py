from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db, bcrypt
from project.models import User, Book
from project.users.forms import RegistrationForm, LoginForm, UpdateAccountForm

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"]) # Permite os métodos GET e POST para essa rota
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form) # Passamos a instância da form para o nosso template


@users.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form) # Passamos a instância da form para o nosso template


@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('your account has been updated', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	return render_template('account.html', title='Account', form=form)

@users.route("/user/<string:username>")
def user_book(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	books = Book.query.filter_by(user=user).order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_books.html', books=books, user=user)
