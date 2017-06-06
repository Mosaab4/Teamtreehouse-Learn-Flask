from flask import jsonify

from flask_restful import Resource

import models


class ReviewList(Resource):
    def get(self):
        return jsonify({'reviews' : [{'course':1, 'rating':5 }]})

class Review(Resource):
    def get(self , id):
        return jsonify({'title': 'Python Basics'})

    def put(self , id):
        return jsonify({'title': 'Python Basics'})

    def delete(self , id):
        return jsonify({'title': 'Python Basics'})
