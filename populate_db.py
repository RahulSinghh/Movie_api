import json
from movie_api.models import Movie, Genre
from movie_api import db


def populate_db():

	with open('./imdb_data.json','r') as f:
		movies = json.load(f)

	for movie in movies:
		new_movie = Movie(popularity = movie['99popularity'], director = movie['director'], imdb_score=movie['imdb_score'],
					 	  name= movie['name'])
		db.session.add(new_movie)
		for g in movie['genre'] :
			print("g" , g)
			gen = Genre(gen = g, movie_genre = new_movie)
			db.session.add(gen)
		
		db.session.commit()
		# print(movie)

if __name__ == '__main__':
    populate_db()
