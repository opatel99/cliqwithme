from cliq import db
from sqlalchemy import literal
from werkzeug.security import check_password_hash, generate_password_hash
import urllib, hashlib
from sqlalchemy.ext.hybrid import hybrid_property
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String)
    year = db.Column(db.String)
    major = db.Column(db.String)
    bio = db.Column(db.String, nullable=True)
    facebook = db.Column(db.String)
    instagram = db.Column(db.String)
    snapchat = db.Column(db.String)
    twitter = db.Column(db.String)
    linkedin = db.Column(db.String)
    phone = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(userID):
        return User.query.get(userID)

    @staticmethod
    def search(searchQuery):
        if searchQuery == "":
            return User.query.all()
        return User.query.filter(User.name.contains(searchQuery)).all()

    @staticmethod
    def friends(userID):
        return Shares.query.filter(Shares.to_userid==userID).all()

    @staticmethod
    def pending(userID):
        return Interactions.query.filter(Interactions.to_userid==userID).filter(Interactions.accepted == None).all()
        
    @hybrid_property
    def pic(self):
        return ("https://www.gravatar.com/avatar/" + hashlib.md5(str(self.email).lower().encode('utf-8')).hexdigest() + "?" + urllib.parse.urlencode({'d':'retro', 's': 300}))
    

class Interactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_userid = db.Column(db.Integer, nullable=False)
    to_userid = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean)

    @staticmethod
    def get_by_id(userID):
        return Interactions.query.get(userID)

class Shares(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_userid = db.Column(db.Integer, nullable=False)
    to_userid = db.Column(db.Integer, nullable=False)
    share = db.Column(db.String)
