from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from store.models import Users

class RegistrationForm(FlaskForm):
	username = StringField("username", validators=[DataRequired(), Length(max=15)])
	email = StringField("email", validators=[DataRequired(), Email()])
	password = StringField("password", validators=[DataRequired()])
	submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
	username = StringField("username", validators=[DataRequired()])
	password = StringField("password", validators=[DataRequired()])
	submit = SubmitField("Log in")

class AddToStockForm(FlaskForm):
	name = StringField("name", validators=[DataRequired()])
	price = StringField("price", validators=[DataRequired()])
	stock = StringField("stock", validators=[DataRequired()])
	submit = SubmitField("Submit")

class AddToCartForm(FlaskForm):
	name = StringField("name", validators=[DataRequired()])
	stock = StringField("stock", validators=[DataRequired()])
	submit = SubmitField("Submit")