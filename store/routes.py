from flask import render_template, redirect, url_for, request
from store.models import Items, Users, Carts, CartItems, StockTable, CartTable
from store.forms import RegistrationForm, LoginForm, AddToStockForm, AddToCartForm
from store import app, db, bc
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
		item = Items.query.filter_by(name=form.name.data).first() 
		if item:
			item.stock += int(form.stock.data)
		else:
			db.session.add(Items(name=form.name.data,price=float(form.price.data),stock=int(form.stock.data)))
		db.session.commit()
		return redirect('/addStock')
	return render_template("addStock.html", form=form)


@app.route('/cart', methods=["Get","POST"])
@login_required
def cart():
	total = 0
	cart = Carts.query.filter_by(user_id=current_user.id).first()
	result = CartItems.query.filter_by(cart_id=current_user.id)
	table = CartTable(result)
	for i in result.all():
		total += Items.query.filter_by(name=i.name).first().price * i.stock
	return render_template("cart.html", table=table, total=total)




@app.route('/addToCart', methods=["Get","POST"])
@login_required
def addToCart():
	form = AddToCartForm()
	if form.validate_on_submit():
		cart = Carts.query.filter_by(user_id=current_user.id).first()
		cartItems = [x.name for x in cart.cartItems]
		item = Items.query.filter_by(name=form.name.data).first()
		print("valid")
		if item and item.stock >= int(form.stock.data):
			if item.name in [x.name for x in cart.cartItems]:
				index = cartItems.index(form.name.data)
				print(type(cart.cartItems[index].stock))
				print(type(form.stock.data))
				cart.cartItems[index].stock += int(form.stock.data)
			else:
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
		db.session.add(Users(email=form.email.data,username=form.username.data,password=bc.generate_password_hash(form.password.data).decode("utf-8")))
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
		if user and bc.check_password_hash(user.password, form.password.data):
			login_user(user,False)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			return redirect('/home')
	return render_template("login.html", form=form)

@app.route('/delCart', methods=["GET","POST"])
@login_required
def delCart():
	form = AddToCartForm()
	if form.validate_on_submit():
		cart = Carts.query.filter_by(user_id=current_user.id).first()
		item = Items.query.filter_by(name=form.name.data).first()
		cartItem = CartItems.query.filter_by(name=form.name.data).first()
		print("valid")
		if cartItem:
			cartItem.stock -= int(form.stock.data)
			item.stock += int(form.stock.data)
			db.session.commit()
			print("succes")
		return redirect('/cart')
	result = Items.query.all()
	table = StockTable(result)
	return render_template("addToCart.html", form=form, table=table)



@app.route('/logout')
def logout():
	logout_user()
	return redirect('/home')

