from movie_api import app
from requests.auth import _basic_auth_str
import unittest


class AuthTest(unittest.TestCase):

	# Check Valid User
	def test_login(self):

		tester 	 = app.test_client(self)
		response = tester.get('/login',headers= {'Authorization':_basic_auth_str('Admin','12345')})
		
		data = response.content_type
		data1 = response.get_json()
		print(response.get_json())

		assert response.status_code == 200
		assert 'json' in data
		assert 'token' in data1

	# Check Fake user Signin Request
	def test_login2(self):
		tester 	 = app.test_client(self)
		response = tester.get('/login',headers= {'Authorization':_basic_auth_str('Fake user','wrong pass')})
		
		data = response.content_type
		data1 = response.get_json()
		print(response.get_json())
		assert response.status_code == 401


	def test_all_users(self):
		# Dummy DATA

		val = {
				    "users": [
				        {
				            "admin": True,
				            "email": "singhrahul1497@gmail.com",
				            "password": "$2b$12$wbaDWlSPeW7k6X5i9OcXHO6ORVMNe2vTV7UxpXV.Cbp0laDh3vjGu",
				            "public_id": "f0bd1cb6-ae3c-4e70-b806-3baeb7f4bcd5",
				            "username": "Rahul"
				        },
				        {
				            "admin": True,
				            "email": "rohit@gmail.com",
				            "password": "$2b$12$lY8iH.5fO5ggfmPHbhI19eb76U8nO.61LNKgXORkTvp3EXhdmuXgu",
				            "public_id": "86679048-b210-4666-ae24-eb8d5e8ab77f",
				            "username": "Admin"
				        },
				        {
				            "admin": False,
				            "email": "notAdmin@gmail.com",
				            "password": "$2b$12$DRhy7193ozCRxdcrpnKRv.CbYUMwikBOJf3ZPiozJYT0cTW8hM3p.",
				            "public_id": "4376f823-5e9b-4045-ab81-d4074510702d",
				            "username": "Non Admin"
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

		headers = {'Authorization':_basic_auth_str('Admin','12345')}
		


		tester 	 	= app.test_client(self)
		response 	= tester.get('/login',headers= {'Authorization':_basic_auth_str('Admin','12345')})
		data     	= response.get_json()
		token 		= data['token']
		print(token)
		
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
		response 	= tester.get('/login',headers= {'Authorization':_basic_auth_str('Non Admin','1234')})
		data     	= response.get_json()
		token 		= data['token']
		print(token)
		
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
		response_type	= response.content_type

		assert response.status_code == 200
		assert "Cannot perform that function!" in response_data
		assert 'json' in response_type


	def test_all_movie(self):
		tester 	 = app.test_client(self)
		response = tester.get('/get_all_movie')
		response_type = response.content_type
		data = response.get_json()
		# print(response)
		assert 'json' in response_type
		assert response.status_code == 200 
		# print(response_type,data.items())


	# Movies with Genre = 'Adventure' Search 
	def test_search_genre(self):
		tester 	 		= app.test_client(self)
		response 		= tester.get('/search/movie_genre/ Fantasy')
		response_type 	= response.content_type
		data 			= response.get_json()
 		content 		= data['Result']
 		print(content)
		# 8 searched of genre were found which are of type text/html

		# Dummy Data
		expected_result = '''[Post('The Wizard of Oz', 'Victor Fleming','8.3','83.0','2021-01-24 18:04:40.198573'), 
		Post('Star Wars', 'George Lucas','8.8','88.0','2021-01-24 18:04:49.826268'), 
		Post('E.T. : The Extra-Terrestrial', 'Steven Spielberg','7.9','79.0','2021-01-24 20:08:09.963947')'''



		assert 'json' in response_type
		assert response.status_code == 200 
		# print(response_type,data.items())

	# # Movies with Movie = 'The Wizard of Oz' Search 
	def test_search_movie(self):
		tester 	 		= app.test_client(self)
		response 		= tester.get('/search/movie_name/The Wizard of Oz')
		response_type 	= response.content_type
		json_data 		= response.get_json()
		content 		= json_data['Result']
 		
		expected_result = "[Post('The Wizard of Oz', 'Victor Fleming','8.3','83.0','2021-01-24 18:04:40.198573')]"

		# 8 searched of genre were found which are of type text/html
		assert 'json' in response_type
		assert response.status_code == 200 
		assert expected_result == content


if __name__ == "__main__":
	unittest.main()