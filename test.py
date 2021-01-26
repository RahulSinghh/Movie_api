from movie_api import app
from requests.auth import _basic_auth_str
import unittest


class AuthTest(unittest.TestCase):

	# Check Valid User
	def test_login(self):

		tester 	 = app.test_client(self)
		response = tester.get('/login',headers= {'Authorization':_basic_auth_str('Admin','admin@123')})
		
		data = response.content_type
		data1 = response.get_json()

		assert response.status_code == 200
		assert 'json' in data
		assert 'token' in data1

	# Check Fake user Signin Request
	def test_login2(self):
		tester 	 = app.test_client(self)
		response = tester.get('/login',headers= {'Authorization':_basic_auth_str('Fake user','wrong pass')})
		
		data = response.content_type
		data1 = response.get_json()
		# print(response.get_json())
		assert response.status_code == 401


	def test_all_users(self):
		# Dummy DATA

		val = {
		    "Users": [
		        {
		            "admin": True,
		            "email": "admin1@gmail.com",
		            "password": "$2b$12$Auxliq26ygnyHDQYzHv7eeYq1gXasquNNpD2WtgfzKnY150ViqZ5m",
		            "public_id": "61cb3b8f-a668-49b5-92f5-d0a707eedd9e",
		            "username": "Admin1"
		        },
		        {
		            "admin": True,
		            "email": "admin@gmail.com",
		            "password": "$2b$12$lRNoMsz.dfPN6xzf516U/OsTXQWq5vr4lDMOb2h2m9KiH4TH1HsuS",
		            "public_id": "2e03a4e7-135b-4a1a-8a2f-92ce88972c03",
		            "username": "Admin"
		        },
		        {
		            "admin": False,
		            "email": "nonadmin@gmail.com",
		            "password": "$2b$12$mONssoHRbhgx9M.xsCUbh.dwJKbPFh8iZUTjpYVQic3LZl9kukfxe",
		            "public_id": "98ad2ef2-60ae-4d90-8026-05ac831cdb19",
		            "username": "Non Admin"
		        },
		        {
		            "admin": False,
		            "email": "nonadmin2@gmail.com",
		            "password": "$2b$12$6kJvfcRWgRXPlnUMsdZCRuOG7OuMScOYIuRgHpI7qYCTlOKwTkIWm",
		            "public_id": "cd55feb4-e07c-4f93-9b34-6bd94de09dc1",
		            "username": "Non Admin2"
		        }
		    ]
		}
		tester 	 = app.test_client(self)
		response = tester.get('/all_users')
		response_type = response.content_type
		data = response.get_json()
		assert val.items() == data.items()
		assert 'json' in response_type

	# Admin Add movie 
	def test_admin_add_movie(self):

		headers = {'Authorization':_basic_auth_str('Admin','admin@123')}
		


		tester 	 	= app.test_client(self)
		response 	= tester.get('/login',headers= {'Authorization':_basic_auth_str('Admin','admin@123')})
		data     	= response.get_json()
		token 		= data['token']
		# print(token)
		
		new_movie_payload = {
		    "99popularity": 79.0,
		    "director": "Steven Spielberg",
		    "genre": [
		      "Adventure",
		      " Drama",
		      " Family",
		      " Fantasy",
		      " Sci-Fi"
		    ],
		    "imdb_score": 7.9,
		    "name": "E.T. : The Extra-Terrestrial"
		}

		headers = {"x-access-token":"{}".format(token)}
		print(headers)

		response 		= tester.post('/add_movie', json= new_movie_payload, headers= headers)
		response_data 	= response.data 
		response_type 	= response.content_type
		assert response.status_code == 200
		assert "Movie created!" in response_data
		assert 'json' in response_type


	# Non Admin Add movie 
	def test_nonadmin_add_movie(self):

		headers = {'Authorization':_basic_auth_str('Non Admin','1234')}
		


		tester 	 	= app.test_client(self)
		response 	= tester.get('/login',headers= {'Authorization':_basic_auth_str('Non Admin','nonadmin@123')})
		data     	= response.get_json()
		token 		= data['token']
		# print(token)
		
		new_movie_payload = {
		    "99popularity": 79.0,
		    "director": "Steven Spielberg",
		    "genre": [
		      "Adventure",
		      " Drama",
		      " Family",
		      " Fantasy",
		      " Sci-Fi"
		    ],
		    "imdb_score": 7.9,
		    "name": "E.T. : The Extra-Terrestrial"
		}

		headers = {"x-access-token":"{}".format(token)}
		# print(headers)

		response 		= tester.post('/add_movie', json= new_movie_payload, headers= headers)
		response_data 	= response.data 
		response_type	= response.content_type

		assert response.status_code == 200
		assert "Cannot perform that function!" in response_data
		assert 'json' in response_type


	def test_all_movie(self):
		tester 	 = app.test_client(self)
		response = tester.get('/all_movies')
		response_type = response.content_type
		data = response.get_json()
		# print(response)
		assert 'json' in response_type
		assert response.status_code == 200 
		# print(response_type,data.items())


	# Movies with Genre = 'Adventure' Search 
	def test_search_genre(self):
		tester 	 		= app.test_client(self)
		response 		= tester.get('/search/movie_genre/Fantasy')
		response_type 	= response.content_type
		data 			= response.get_json()
 		content 		= data
 		# print(content.items)
		# 8 searched of genre were found which are of type text/html

		# Dummy Data
		expected_result = {
		    "Count of result": 4,
		    "Result": [
		        {
		            "date_added": "Tue, 26 Jan 2021 16:13:08 GMT",
		            "director": "J. Searle Dawley",
		            "imdb_score": 6.4,
		            "movie_id": 15,
		            "name": "Snow White",
		            "popularity": 64.0
		        },
		        {
		            "date_added": "Tue, 26 Jan 2021 16:13:09 GMT",
		            "director": "F.W. Murnau",
		            "imdb_score": 8.1,
		            "movie_id": 56,
		            "name": "Nosferatu, eine Symphonie des Grauens",
		            "popularity": 81.0
		        },
		        {
		            "date_added": "Tue, 26 Jan 2021 16:13:09 GMT",
		            "director": "Tod Browning",
		            "imdb_score": 7.7,
		            "movie_id": 63,
		            "name": "Dracula",
		            "popularity": 77.0
		        },
		        {
		            "date_added": "Tue, 26 Jan 2021 16:13:10 GMT",
		            "director": "Carl Boese",
		            "imdb_score": 7.4,
		            "movie_id": 128,
		            "name": "Der Golem, wie er in die Welt kam",
		            "popularity": 74.0
		        }
		    ]
		}



		assert 'json' in response_type
		assert response.status_code == 200
		assert expected_result.items() == content.items()
		# print(response_type,data.items())

	# # Movies with Movie = 'The Wizard of Oz' Search 
	def test_search_movie(self):
		tester 	 		= app.test_client(self)
		response 		= tester.get('/search/movie_name/The Wizard of Oz')
		response_type 	= response.content_type
		json_data 		= response.get_json()
		content 		= json_data
		print(content.items())
 		
		expected_result = {
		    "Result": [
		        {
		            "date_added": "Tue, 26 Jan 2021 16:13:08 GMT",
		            "director": "Victor Fleming",
		            "genre": [
		                "Adventure",
		                " Family",
		                " Fantasy",
		                " Musical"
		            ],
		            "imdb_score": 8.3,
		            "movie_id": 1,
		            "name": "The Wizard of Oz",
		            "popularity": 83.0
		        },
		        {
		            "date_added": "Tue, 26 Jan 2021 16:13:08 GMT",
		            "director": "Larry Semon",
		            "genre": [
		                "Comedy",
		                " Family",
		                " Fantasy",
		                " Adventure"
		            ],
		            "imdb_score": 5.3,
		            "movie_id": 37,
		            "name": "The Wizard of Oz",
		            "popularity": 53.0
		        }
		    ]
		}

		# 8 searched of genre were found which are of type text/html
		assert 'json' in response_type
		assert response.status_code == 200 
		assert expected_result.items() == content.items()


if __name__ == "__main__":
	unittest.main()