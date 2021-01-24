from movie_api import app
import unittest


class AuthTest(unittest.TestCase):

	def test_index(self):
		login_payload = {
			'username' : 'Non Admin',
			'password' : '1234'
		}

		tester 	 = app.test_client(self)
		response = tester.get('/login')
		print("Hello",response)
		data = response.json()
		print(data)


if __name__ == "__main__":
	unittest.main()