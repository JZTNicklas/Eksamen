from flask import flash, render_template, redirect, url_for, request, make_response
from store.models import Items, Users, databaseResults
from store import app, db

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
