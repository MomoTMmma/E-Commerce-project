from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
db = SQLAlchemy()

cart = db.Table(
    'cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user_id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('product_id'), nullable=False)
)
# may need to change product_id name
#  
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50), nullable=False, )
    last_name = db.Column(db.String(50), nullable=False, )
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, )


    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def saveUser(self):
        db.session.add(self)
        db.session.commit()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True )
    price = db.Column(db.Numeric(10,2))
    description = db.Column(db.String)
    category = db.Column(db.String)
    img_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    carted = db.relationship('User',
        secondary = 'cart',
        backref = 'carted',
        lazy = 'dynamic'
    )


    def __init__(self, title, price, description, category, img_url, user_id):
        self.title = title
        self.price = price
        self.description = description
        self.category = category
        self.img_url = img_url
        self.user_id = user_id

    

    def saveCarted(self, user):
        self.carted.append(user)
        db.session.commit()

    def deleteCarted(self, user):
        self.carted.delete(user)
        db.session.commit()
        
    def saveChanges(self):
        db.session.commit()

    def saveProduct(self):
        db.session.add(self)
        db.session.commit()

    def deleteProduct(self):
        db.session.delete(self)
        db.session.commit()
    
  
    def to_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'product_id' : self.product_id,
            'price' : self.price,
            'description' : self.description,
            'category' : self.category,
            'img_url' : self.img_url,           
            'item' : self.item.username

        }
