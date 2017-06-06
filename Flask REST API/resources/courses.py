from flask import jsonify , Blueprint, url_for , abort

from flask_restful import Resource ,Api , reqparse ,inputs ,fields , marshal , marshal_with


import models

course_field = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'reviews': fields.List(fields.String)
}

def add_reviews(course):
    course.reviews = [url_for('resourse.reviews.review', id = review.id) for review in 
    course.review_set]

    return course

def course_or_404(course_id):
    try:
        course = models.Course.get(models.Course.id == course_id)

    except model.Course.DoesNotExist :
        abort(404 ,message = "Course {} does not exist".format(course_id))

    else:
        return course

class CourseList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required = True,
            help = 'No course title provided',
            location = ['from','json']
        )
        self.reqparse.add_argument(
            'url',
            help = 'No course url provided',
            required = True,
            location = ['form' , 'json'],
            type = inputs.url        
        )
        #super(CourseList,self).__init__() 

    def get(self):
        courses = [marshal(add_reviews(course), course_field) for course in models.Course.select()]
        return {'courses': courses}

    def post(self):
        args = self.reqparse.parse_args()
        models.Course.create(**args)
        return jsonify({'courses' : [{'title': 'Python Basics'}]})
        
class Course(Resource):
    @marshal_with(course_field) #instead of using marshal function
    def get(self , id):
        return add_reviews(course_or_404(id))

    def put(self , id):
        return jsonify({'title': 'Python Basics'})

    def delete(self , id):
        return jsonify({'title': 'Python Basics'})

courses_api = Blueprint('resource.courses', __name__)
api = Api(courses_api)

api.add_resource(
    CourseList,
    '/api/v1/courses',
    endpoint = 'courses'
)

api.add_resource(
    Course,
    '/api/v1/courses/<int:id>',
    endpoint = 'course'
)