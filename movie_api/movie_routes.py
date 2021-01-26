from flask import  flash, request, abort,  make_response, jsonify
from movie_api.models import Movie, Genre
from flask_sqlalchemy import SQLAlchemy
from admin_routes import token_required
from movie_api import app, db


@app.route('/all_movies', methods=['GET'])
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
        genre_list = []
        for genre in movie.genres:
            genre_list.append(genre.gen)
        movie_data['genre'] = genre_list
        output.append(movie_data)

    return jsonify({'movies' : output})


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
            for g in data['genre']:
                gen = Genre(gen = g , movie_genre = movie)
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


@app.route('/movie/<movie_id>', methods=['GET'])
@token_required
def get_one_movie(current_user, movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()

    if not movie:
        return jsonify({'message' : 'No movie found!'})

    movie_data = {}
    movie_data['movie_id']   = movie.movie_idmovies
    movie_data['name']       = movie.username
    movie_data['director']   = movie.director
    movie_data['imdb_score'] = movie.imdb_score
    movie_data['popularity'] = movie.imdb_score
    movie_data['date_added'] = movie.date_added

    return jsonify(movie_data)


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
	

