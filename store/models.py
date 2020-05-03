from store import db, login_manager
from flask_table import Table, Col
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

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

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	username = db.Column(db.String, unique=True)
	admin = db.Column(db.Boolean,default=False)
	cart = db.relationship("Carts", backref="users",lazy=True)

	def __repr__(self):
		return self.email

	def getPassword(self):
		return self.password

	def isAdmin(self):
		return self.admin


class Carts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cartItems = db.relationship("CartItems", backref="carts",lazy=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

	def __repr__(self):
		return str(self.user_id)

class CartItems(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String, nullable=False)
	stock = db.Column(db.String, nullable=False)
	cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)

	def __repr__(self):
		return self.name

class StockTable(Table):
	id = Col('id', show=False)
	name = Col('Name')
	price = Col('Price')
	stock = Col('Stock')

class CartTable(Table):
	id = Col('id', show=False)
	name = Col('Name')
	price = Col('Price')
	stock = Col('Stock')