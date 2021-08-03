from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)

	bcrypt.init_app(app)
	login_manager.init_app(app)

	from project.users.routes import users
	from project.books.routes import books
	from project.main.routes import main
	from project.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(main)
	app.register_blueprint(books)
	app.register_blueprint(errors)

    # creating tables (run at first time)
	# db.create_all(app=app)

	return app
