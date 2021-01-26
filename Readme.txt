##############################################
Main file to run the application
##############################################

i) python app.py ------ This file will host the API 
ii) Test.py      ------ Test cases which describes the various functionality required for API

Login using /login to get the token, click on header in Postman, Under key write 'x-access-token' and in value paste the token


##############################################
 Different Routes for various functionily
##############################################

i) '/all_users' (GET)      							--------- To list all registererd users in the database
ii '/register_user' (POST) 							--------- Users registers himself, Initially Users will be assisgned Non-Admin privileges
iii) '/user/<public_id>' (PUT) 						--------- Existing Admin User can promote any other user to admin privileges
iv) '/user/<public_id>' (DELETE)					--------- Admin User can delete any other user.
v) '/login' 										--------- Login for users, X access token will be given to user valid for 30 mins
vi) '/get_all_movie' (GET)							--------- To get list of all movies in database, Everyone can access the list
vii) /movie/<movie_id>' (GET) 						--------- To get a movie with a particular movie id 
viii) '/add_movie' (POST)							--------- To add new movie , only admin access , Login token required.
ix) /movie/<int:movie_id>/update (POST) 			--------- To update already existing movie, only admin access.login token required. 
x) '/movie/<movie_id>' (DELETE) 					--------- To delete already existing movie, only admin access.login token required. 
xi) '/search/movie_name/<string:movie_name>' (GET)  --------- To search already existing movie on basis of movie ID, All access.login token required.
x) '/search/movie_genre/<string:genre_name>' (GET)  --------- To search already existing movie on basis of GENRE, All access.login token required.