from flask import flash, render_template, redirect, url_for, request, make_response
from store.models import Items, Users, databaseResults
from store.forms import RegistrationForm, LoginForm
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


@app.route('/signup', methods=["GET","POST"])
def signup():
	form=RegistrationForm()
	if form.validate_on_submit():
		if form.username.data != Users.query.filter_by(username=form.username.data).first:
			if form.email.data != Users.query.filter_by(email=form.email.data).first:
				user = Users(email=form.email.data,username=form.username.data,password=form.password.data)
				db.session.add(user)
				db.session.commit()
				return redirect('/login')
			else:
				return render_template("signup.html", form=form)
		
	


@app.route('/login', methods=["GET","POST"])
def login():
	form=LoginForm()
	return render_template("login.html", form=form)
