from flask import jsonify , Blueprint, url_for , abort

from flask_restful import Resource ,Api , reqparse ,inputs ,fields , marshal , marshal_with


import models

course_fields = {
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

    except models.Course.DoesNotExist :
        abort(404)

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
        courses = [marshal(add_reviews(course), course_fields) for course in models.Course.select()]
        return {'courses': courses}

    @marshal_with(course_fields)
    def post(self):
        args = self.reqparse.parse_args()
        course = models.Course.create(**args)
        return (add_reviews(course), 201, {
                'Location': url_for('resources.courses.course', id=course.id)}
               )
        
class Course(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required = True,
            help = "No course title provided",
            location = ['form' , 'json']
        )

        self.reqparse.add_argument(
            'url',
            required = True,
            help = "No Course Url Provided",
            location = ['form' , 'json'],
            type = inputs.url
        )

    @marshal_with(course_fields) #instead of using marshal function
    def get(self , id):
        #return marshal(add_reviews(course_or_404(id)) , course_fields) using marshal
        return add_reviews(course_or_404(id)) 

    @marshal_with(course_fields)  
    def put(self , id):
        args = self.reqparse.parse_args()
        query = models.Course.update(**args).where(models.Course.id == id )
        query.execute()
        
        return (add_reviews(models.Course.get(models.Course.id == id )) , 200 ,
                {'Location': url_for('resources.courses.course' , id =id)}) #status code then additional headers

    def delete(self , id):
        query = models.Course.delete().where(models.Course.id == id )
        query.execute()
        
        return ('', 204 ,{'Location': url_for('resources.courses.courses' , id =id)}) 


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