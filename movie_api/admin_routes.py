from movie_api.models import User
from flask_login import login_user, current_user,logout_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import  flash, request, abort,  make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from movie_api import app, db, bcrypt
from functools import wraps
import datetime
import uuid
import jwt

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
            return jsonify({'message' : 'Token is not valid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def home():
    return jsonify({"Message" : "Login using /login get the token, click on header in Postman, Under key write 'x-access-token' and in value paste the token"})


@app.route('/all_users', methods=['GET'])
def all_users():

    users = User.query.all()

    result = []

    for user in users:
        user_data = {}
        user_data['email'] = user.email
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        result.append(user_data)

    return jsonify({'Users' : result})


@app.route('/register_user', methods=['POST'])
@token_required
def register_user():
    if not current_user.admin:
        return jsonify({'message' : 'Non Admin cannot perform that action'})

    data = request.get_json()

    hashed_password = str(bcrypt.generate_password_hash(data['password']))
    username  =  str(data['username'])
    email     = str(data['email'])
    public_id = str(uuid.uuid4())

    new_user  = User(public_id=public_id, username=username, email = email,
    				password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Non Admin cannot perform that action'})

    user 		= User.query.filter_by(public_id=public_id).first()
    username	= user.username

    if not user:
        return jsonify({'message' : 'User Not found'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'User {} has been promoted!'.format(username)})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Non Admin cannot perform that action'})

    user 		= User.query.filter_by(public_id=public_id).first()
    username	= user.username

    if not user:
        return jsonify({'message' : 'No user found'})

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