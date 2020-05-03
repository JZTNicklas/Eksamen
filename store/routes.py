from flask import render_template, redirect, url_for, request, make_response
from store.models import Items, Users, Carts, CartItems, StockTable, CartTable
from store.forms import RegistrationForm, LoginForm, AddToStockForm, AddToCartForm
from store import app, db
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/stock')
@login_required
def stock():
	result = Items.query.all()
	table = StockTable(result)
	return render_template("stock.html", table=table)

@app.route('/addStock', methods=["Get","POST"])
@login_required
def addStock():
	form=AddToStockForm()
	if form.validate_on_submit():
		print("Valid")
		db.session.add(Items(name=form.name.data,price=float(form.price.data),stock=int(form.stock.data)))
		db.session.commit()
		return redirect('/addStock')
	return render_template("addStock.html", form=form)

@app.route('/cart', methods=["Get","POST"])
@login_required
def cart():
	result = CartItems.query.filter_by(cart_id=current_user.id)
	table = CartTable(result)
	return render_template("cart.html", table=table)


@app.route('/addToCart', methods=["Get","POST"])
@login_required
def addToCart():
	form = AddToCartForm()
	if form.validate_on_submit():
		cart = Carts.query.filter_by(user_id=current_user.id).first()
		item = Items.query.filter_by(name=form.name.data).first()
		print("valid")
		if item and str(item.stock) > form.stock.data:
			db.session.add(CartItems(name=form.name.data,stock=int(form.stock.data),cart_id=cart.id))
			item.stock -= int(form.stock.data)
			db.session.commit()
			print("succes")
			return redirect('/cart')
	result = Items.query.all()
	table = StockTable(result)
	return render_template("addToCart.html", form=form, table=table)


@app.route('/signup', methods=["GET","POST"])
def signup():
	form=RegistrationForm()
	if form.validate_on_submit():
		if Users.query.filter_by(username=form.username.data).first():
			return render_template("signup.html", form=form)
		if Users.query.filter_by(email=form.email.data).first():
			return render_template("signup.html", form=form)	
		db.session.add(Users(email=form.email.data,username=form.username.data,password=form.password.data))
		db.session.commit()
		user = Users.query.filter_by(username=form.username.data).first() 


		db.session.add(Carts(user_id=user.id))
		db.session.commit()


		return redirect('/login')
	return render_template("signup.html", form=form)

@app.route('/login', methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user and form.password.data == user.password:
			login_user(user,False)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			return redirect('/home')
	return render_template("login.html", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/home')

