from flask import jsonify , Blueprint , url_for ,abort

from flask_restful import (Resource , Api ,reqparse , inputs, fields , marshal , marshal_with ,inputs)

import models

review_fields = {
    'id':fields.String,
    'for_course':fields.String,
    'rating' :fields.Integer,
    'comment' :fields.String(default=''),
    'created_at' :fields.DateTime
}

def review_or_404(review_id):
    try :
        review = models.Course.get(models.Review.id == review_id)
    
    except models.Review.DoesNotExist:
        abort(404)
        
    else:
        return review

def add_course(review):
    review.for_course = url_for('resource.courses.course' , id = review.course.id)
    return review


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
        #super(ReviewList,self).__init__() 
    def get(self):
        return { 'reviews' : [
            marshal(add_course(review),review_fields) for review in models.Review.select()
        ]}
    
    @marshal_with(review_fields)
    def post(self):
        args = self.reqparse.parse_args()
        review = models.Review.create(**args)
        return (add_course(review), 201 ,{
            'Location' :url_for('resource.reviews.review' ,id = review.id)
        })
class Review(Resource):
    @marshal_with(review_fields)
    def get(self , id):
        return add_course(review_or_404(id))

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