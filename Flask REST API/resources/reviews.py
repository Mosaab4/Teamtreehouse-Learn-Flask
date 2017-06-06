from flask import jsonify , Blueprint

from flask_restful import Resource , Api ,reqparse , inputs

import models


class ReviewList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'course',
            type = inputs.positive,
            required = True,
            help = "No Course Provided",
            location = ['form' , 'json']
        )
        self.reqparse.add_argument(
            'rating',
            type = inputs.int_range(1,5),
            required = True,
            help = 'No Rating Provided',
            location = ['form','json']
        )
        self.reqparse.add_argument(
            'comment',
            required = False,
            nullable = True,
            location = ['form','json'],
            default = ''
        )
        super(ReviewList,self).__init__() 
    def get(self):
        return jsonify({'reviews' : [{'course':1, 'rating':5 }]})

class Review(Resource):
    def get(self , id):
        return jsonify({'title': 'Python Basics'})

    def put(self , id):
        return jsonify({'title': 'Python Basics'})

    def delete(self , id):
        return jsonify({'title': 'Python Basics'})


reviews_api = Blueprint('resources.reviews', __name__)
api = Api(reviews_api)

api.add_resource(
    ReviewList,
    '/reviews',
    endpoint = 'reviews'
)

api.add_resource(
    Review,
    '/reviews/<int:id>',
    endpoint = 'review'
)