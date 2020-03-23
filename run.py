from flask import Flask, flash, render_template, redirect, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

class Items(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	price = db.Column(db.Float)
	stock = db.Column(db.Integer)
	
	def __repr__(self):
		return self.name

	def getStock(self):
		return self.stock

	def getPrice(self):
		return self.price

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	username = db.Column(db.String, unique=True)
	admin = db.Column(db.Boolean,default=False)


	def __repr__(self):
		return self.email

	def getPassword(self):
		return self.password

	def isAdmin(self):
		return self.admin

class databaseResults(Table):
    id = Col('id', show=False)
    name = Col('Name')
    price = Col('Price')
    stock = Col('Stock')

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/stock')
def stock():
	result = Items.query.all()
	table = databaseResults(result)
	return render_template("stock.html", table=table)

@app.route('/addStock')
def addStock():
	name = request.args.get("name")
	price = request.args.get("price")
	stock = request.args.get("stock")
	if type(name) == str and type(price) == str and type(stock) == str:
		db.session.add(Items(name=name,price=float(price),stock=int(stock)))
		db.session.commit()
		return redirect('/addStock')
	return render_template("addStock.html")

@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/checkLogin')
def checkLogin():
	username = request.args.get("username")
	password = request.args.get("password")
	print(username)
	print(password)
	if type(username) == str and type(password) == str:
		user = Users.query.filter(Users.username==username).first() 
		if user.password == password:
			print("Succesfull")
			return redirect('/home')
		else:
			print("Failed")
			return redirect('/login')

@app.route('/signup')
def signup():
	return render_template("signup.html")

@app.route('/checkSignup')
def checkSignup():
	email = request.args.get("email")
	username = request.args.get("username")
	password = request.args.get("password")
	print(email)
	print(password)
	print(username)
	if type(username) == str and type(password) == str and type(email) == str:
		print("ran")
		for user in Users.query.all():
			if username != user.username and email != user.email:
				db.session.add(Users(email=email,password=password,username=username))
				db.session.commit()
				print("Succesfull")
				return redirect('/login')
	print("Failed")
	return redirect('/signup')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')