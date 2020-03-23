from store import db
from flask_table import Table, Col

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
