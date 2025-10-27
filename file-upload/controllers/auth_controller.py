from flask import Blueprint, request, jsonify
import logging
import datetime
from config import Config
import jwt

auth_bp = Blueprint('auth_bp', __name__)

#POST - for login request
@auth_bp.route('/login', methods = ['POST'])
def login():
    credentials = request.get_json()

    if not credentials or not credentials.get('username') or not credentials.get('password'):
        logging.warning(f"Empty fields")
        return jsonify({'message': 'Username and password are required'}), 400
    
    username = credentials['username']
    password = credentials['password']

    if username == 'admin' and password == 'admin':
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        }, Config.SECRET_KEY, algorithm = 'HS256')
        logging.info(f'[LOGIN SUCCESS] Username: {username}')
        return jsonify({f'message': 'Login Successful', 'token': token}), 200
    
    logging.warning(f'[LOGIN FAILED] Username: {username}')
    return jsonify({'message': 'Invalid credentials'}), 401



