from movie_api import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id          = db.Column(db.Integer, primary_key = True, unique = True)
	public_id 	= db.Column(db.String(50), unique=True)
	username 	= db.Column(db.String(20), unique=True, nullable = False)
	email    	= db.Column(db.String(60), unique=True, nullable = False)
	password 	= db.Column(db.String(80), nullable = False)
	admin		= db.Column(db.Boolean)

	def __repr__(self):
		return "User('{}', '{}' , '{}')".format(self.username, self.email, self.admin)



class Movie(db.Model):
	movie_id 	= db.Column(db.Integer, primary_key=True)
	popularity 	= db.Column(db.Float, nullable = False)
	director  	= db.Column(db.String(100), nullable = False)
	imdb_score 	= db.Column(db.Float, nullable = False)
	name 		= db.Column(db.String(100), nullable = False)
	date_added 	= db.Column(db.DateTime, nullable = False, default=datetime.utcnow)	 
	genres 		= db.relationship('Genre', backref='movie_genre', lazy = True )
	def __repr__(self):
		return "Post('{}', '{}','{}','{}','{}')".format(self.name,self.director,self.imdb_score,
														self.popularity, self.date_added)

class Genre(db.Model):
	id = db.Column(db.Integer , primary_key=True)
	gen = db.Column(db.String(50), nullable = False)
	mov_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'),nullable=False)
	
	def __repr__(self):
		return "Post('{}', '{}' )".format(self.gen,self.mov_id)