from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	author = StringField('Author', validators=[DataRequired()])
	pdfile = FileField('Book', validators=[FileAllowed(['pdf'])])
	submit = SubmitField('Submit')
