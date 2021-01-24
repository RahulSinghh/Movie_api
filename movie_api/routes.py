from flask import  flash, redirect, request, abort,  make_response
from movie_api import app, db, bcrypt
from movie_api.models import User, Movie, Genre
from flask_login import login_user, current_user,logout_user,login_required

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

from flask import jsonify
import jwt
import uuid
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/all_users', methods=['GET'])
def all_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['email'] = user.email
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})


@app.route('/register_user', methods=['POST'])
# @token_required
def register_user():#(current_user):

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = str(bcrypt.generate_password_hash(data['password']))
    username =  str(data['username'])
    email    = str(data['email'])
    public_id = str(uuid.uuid4())
    print(str(uuid.uuid4()))
    new_user = User(public_id=public_id, username=username, email = email,
    				password=hashed_password, admin=data['admin'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user 		= User.query.filter_by(public_id=public_id).first()
    username	= user.username

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'User {} has been promoted!'.format(username)})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user 		= User.query.filter_by(public_id=public_id).first()
    username	= user.username

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'User {} has been deleted!'.format(username)})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/get_all_movie', methods=['GET'])
def get_all_movie():
    movies= Movie.query.all()

    output = []

    for movie in movies:
        movie_data = {}
        movie_data['movie_id'] 	 = movie.movie_id
        movie_data['name'] 		 = movie.name
        movie_data['director'] 	 = movie.director
        movie_data['imdb_score'] = movie.imdb_score
        movie_data['popularity'] = movie.popularity
        movie_data['date_added'] = movie.date_added
        output.append(movie_data)

    return jsonify({'movies' : output})

@app.route('/movie/<movie_id>', methods=['GET'])
@token_required
def get_one_movie(current_user, movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()

    if not movie:
        return jsonify({'message' : 'No movie found!'})

    movie_data = {}
    movie_data['movie_id'] 	 = movie.movie_idmovies
    movie_data['name'] 		 = movie.username
    movie_data['director'] 	 = movie.director
    movie_data['imdb_score'] = movie.imdb_score
    movie_data['popularity'] = movie.imdb_score
    movie_data['date_added'] = movie.date_added

    return jsonify(movie_data)

@app.route('/add_movie', methods=['POST'])
@token_required
def add_movie(current_user):
	data = request.get_json()

	if current_user.admin: 
		new_movie = Movie(popularity =data['99popularity'], director = data['director'], imdb_score=data['imdb_score'],
					 	  name= data['name'])
		db.session.add(new_movie)
		for g in data['genre'] :
			print("g" , g)
			gen = Genre(gen = g, movie_genre = new_movie)
			db.session.add(gen)
		
		db.session.commit()
		return jsonify({'message' : "Movie created!"})
	else:
		return jsonify({'message' : "Cannot perform that function!"})


@app.route('/movie/<int:movie_id>/update', methods=['POST'])
@token_required
def update_movie(current_user,movie_id):
	movie = Movie.query.filter_by(movie_id=movie_id).first()

	if not movie:
		return jsonify({'message' : 'No movie found!'})

	data = request.get_json()
	if current_user.admin:
		if '99popularity' in data:
			movie.popularity = data['99popularity']
		if 'name' in data:
			movie.name = data['name']
		if 'imdb_score' in data :
			movie.imdb_score = data['imdb_score']
		if 'director' in data:
			movie.director = data['director']
		if 'genre' in data :
			gen = Genre(gen = g , movie_genre = new_movie)
			db.session.add(gen)
		db.session.commit()
		return jsonify({'message' : 'Movie {} Updated!'.format(movie.movie_id)})
	else:
		return jsonify({'message' : 'Cannot perform that function!'})



@app.route('/movie/<movie_id>', methods=['DELETE'])
@token_required
def delete_movie(current_user, movie_id):
	movie = Movie.query.filter_by(movie_id=movie_id).first()

	if not movie:
		return jsonify({'message' : 'No movie found!'})

	if current_user.admin:
		db.session.delete(movie)
		db.session.commit()
		return jsonify({'message' : 'Movie deleted!'})
	else:
		return jsonify({'message' : 'Cannot perform that function!'})


@app.route('/search/movie_name/<string:movie_name>')
def search_movie(movie_name):
	movie = Movie.query.filter_by(name=movie_name).all()
	print(movie)
	if movie:
		return jsonify({'Result' : str(movie)})
	else :
		return jsonify({'Result' : 'No movie found!'})


@app.route('/search/movie_genre/<string:genre_name>')
def search_genre(genre_name):
	genre = Genre.query.filter_by(gen=genre_name).all()
	search = []
	for gen in genre :
		search.append(gen.movie_genre)
	if genre:
		return jsonify({'Result' : str(search)})
	else :
		return jsonify({'Result' : 'No movie found!'})
	

