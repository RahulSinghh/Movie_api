from flask import render_template, url_for, flash, redirect, request, abort
from movie_api import app, db, bcrypt
from movie_api.models import User, Movie
from flask_login import login_user, current_user,logout_user,login_required
import os, binascii
from PIL import Image

from flask import jsonify

# app.route("/")
# @app.route("/home",  methods=['GET'])
# def home():
#     movies = Movie.query.all()
#     output = [] 
#     for movie in movies:
#     	movie_data = {}
#     	movie_data['popularity']= movie.popularity
#     	movie_data['imdb_score']= movie.imdb_score
#     	movie_data['name'] 		= movie.name
#     	movie_data['director'] 	= movie.director
#     	output.append(movie_data)

#     return jsonify({'movies':output})

# app.route("/")
# @app.route("/all_users",  methods=['GET'])
# def all_users():
#     users = User.query.all()
#     output = [] 
#     for user in users:
#     	user_data = {}
#     	user_data['username']	= user.username
#     	user_data['email']		= user.email
#     	user_data['admin'] 		= user.admin
#     	output.append(user_data)

#     return jsonify({'users':output})



# @app.route("/register", methods=['POST'])
# def register():
#     if current_user.is_authenticated:
#         return jsonify({'Message':'User {} is already Logged in!!'.format(current_user.username)})

#     username = request.json.get('username')
#     password = request.json.get('password')
#     email  	 = request.json.get('email')
#     admin	 = request.json.get('Admin')

#     if username is None or password is None or username == "" or password == "":
#     	return jsonify({'Message':'Bad Input!!'})
#     if User.query.filter_by(username = username).first() is not None:
#     	return jsonify({'Message':'User with same Username already exists!!'})
#     if User.query.filter_by(email = email).first() is not None:
#     	return jsonify({'Message':'User with same Email already exists!!'})
#     hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
#     user_1 = User(username = username, email = email, password = hash_password, admin= admin)
#     db.session.add(user_1)
#     db.session.commit()
#     return jsonify({'Message':'New User is created !!'})
   

# @app.route("/login", methods=['POST'])
# def login():
#     if current_user.is_authenticated:
#         return jsonify({'Message':'User {} is already Logged in!!'.format(current_user.username)})
#     data = request.get_json()
#     if data:
#         user = User.query.filter_by(email = data['email']).first()
#         if user and bcrypt.check_password_hash(user.password, data['password']):
#             login_user(user)
#             return jsonify({'Message':'User {} Logged in!!'.format(current_user.username)})
#         else:
#             return jsonify({'Login Unsuccessful. Please check username and password'})

#     return jsonify({'Login Unsuccessful. Please check username and password'})


# @app.route("/logout",methods=['GET'])
# def logout():
#     logout_user()
#     return jsonify({'Message':'Current User Logged out successfully!!'})



# @app.route("/add_movie", methods=['POST'])
# @login_required
# def add_movie():
# 	data = request.get_json()
# 	if data:
# 		movie    = Movie(name=data['name'], director=data['director'], 
# 						imdb_score=data['imdb_score'], popularity=data['popularity'] )
# 		db.session.add(movie)
# 		db.session.commit()
# 		return jsonify({'Message':'Your post has been created!'})

# 	return jsonify({'Message':'Movie was not added'})   
   	



@app.route('/login')
def login():
	auth = req
