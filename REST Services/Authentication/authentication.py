# Importing necessary libraries
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import pandas as pd
import bcrypt

# Creating the Flask application
app = Flask(__name__)
api = Api(app)

# Defining the Register class for user registration
class Register(Resource):
    def post(self):
        # Using reqparse to parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        # Reading user data from the CSV file
        data = pd.read_csv('users.csv')
        if args['username'] in data['username'].values:
            return {'message': 'User already exists'}, 400

        # Hashing the password and adding the new user to the CSV file
        hashed_pw = bcrypt.hashpw(args['password'].encode('utf8'), bcrypt.gensalt())
        new_data = pd.DataFrame({
            'username': [args['username']],
            'password': [hashed_pw.decode('utf8')]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'message': 'User registered successfully'}, 201

# Defining the Login class for user login
class Login(Resource):
    def post(self):
        # Using reqparse to parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        # Reading user data from the CSV file
        data = pd.read_csv('users.csv')
        user = data[data['username'] == args['username']]

        if user.empty:
            return {'message': 'User not found'}, 404

        # Checking the password
        if bcrypt.checkpw(args['password'].encode('utf8'), user.iloc[0]['password'].encode('utf8')):
            return {'message': 'Login successful'}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

# Defining the User class for updating and deleting users
class User(Resource):
    def put(self, name):
        # Using reqparse to parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        # Reading user data from the CSV file
        data = pd.read_csv('users.csv')
        user = data[data['username'] == name]

        if user.empty:
            return {'message': 'User not found'}, 404

        # Hashing the password and updating the user
        data.loc[data['username'] == name, 'password'] = bcrypt.hashpw(args['password'].encode('utf8'), bcrypt.gensalt()).decode('utf8')
        data.to_csv('users.csv', index=False)
        return {'message': 'User updated successfully'}, 200

    def delete(self, name):
        # Reading user data from the CSV file
        data = pd.read_csv('users.csv')
        data = data[data['username'] != name]
        data.to_csv('users.csv', index=False)
        return {'message': 'User deleted successfully'}, 200

# Defining the Users class for listing users
class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

# Adding the defined resources to the API
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(User, '/user/<string:name>')
api.add_resource(Users, '/users')

# Running the application
if __name__ == '__main__':
    app.run(debug=True)
