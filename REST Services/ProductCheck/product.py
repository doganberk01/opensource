# Importing necessary libraries
from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd

# Creating the Flask application
app = Flask(__name__)
api = Api(app)

# Defining the Products class for listing and adding products
class Products(Resource):
    def get(self):
        # Reading product data from the CSV file
        data = pd.read_csv('products.csv')
        # Converting data to dictionary format
        data = data.to_dict('records')
        # Returning data and HTTP status code
        return {'data': data}, 200

    def post(self):
        # Using reqparse to parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('price', required=True, type=float)
        parser.add_argument('quantity', required=True, type=int)
        args = parser.parse_args()

        # Reading product data from the CSV file
        data = pd.read_csv('products.csv')
        # Creating new product data in DataFrame format
        new_data = pd.DataFrame({
            'name': [args['name']],
            'price': [args['price']],
            'quantity': [args['quantity']]
        })
        # Adding new product to existing data
        data = pd.concat([data, new_data], ignore_index=True)
        # Saving data to the CSV file
        data.to_csv('products.csv', index=False)
        # Returning new product data and HTTP status code
        return {'data': new_data.to_dict('records')}, 201

# Defining the Product class for updating and deleting products
class Product(Resource):
    def put(self, name):
        # Using reqparse to parse incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('price', required=True, type=float)
        parser.add_argument('quantity', required=True, type=int)
        args = parser.parse_args()

        # Reading product data from the CSV file
        data = pd.read_csv('products.csv')
        # Finding the product to be updated
        product = data[data['name'] == name]

        if product.empty:
            # Returning error message if product is not found
            return {'message': 'Product not found'}, 404

        # Updating product price and quantity
        data.loc[data['name'] == name, 'price'] = args['price']
        data.loc[data['name'] == name, 'quantity'] = args['quantity']
        # Saving data to the CSV file
        data.to_csv('products.csv', index=False)
        # Returning success message and HTTP status code
        return {'message': 'Product updated successfully'}, 200

    def delete(self, name):
        # Reading product data from the CSV file
        data = pd.read_csv('products.csv')
        # Removing the product from the data
        data = data[data['name'] != name]
        # Saving data to the CSV file
        data.to_csv('products.csv', index=False)
        # Returning success message and HTTP status code
        return {'message': 'Product deleted successfully'}, 200

# Adding the defined resources to the API
api.add_resource(Products, '/products')
api.add_resource(Product, '/product/<string:name>')

# Running the application
if __name__ == '__main__':
    app.run(debug=True)
