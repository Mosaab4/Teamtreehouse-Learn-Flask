from peewee import *

db = SqliteDatabase('students.db')

class Student(Model):
    username = CharField(max_length = 255 , unique = True)
    points = IntegerField(default = 0)

    #the 2nd class told the model What DB it belongs to 
    class Meta:
        database = db


students = [
    {
        'username': 'keneethlove',
        'points': 4888
    },
    {
        'username':'chalkers',
        'points':11912
    },
    {
        'username': 'joykwsten2',
        'points':7363
    },
    {
        'username': 'craigsdennis',
        'points': 4079
    },
    {
        'username': 'davemcfarland',
        'points': 14717
    }
]

def add_students():
    for student in students:
        try:
            Student.create(username = student['username'],
                        points = student['points'])
        except IntegrityError:
            student_record = Student.get(username = student['username'])
            student_record.points = student['points']
            student_record.save()

def top_student():
    #sort all students by points desc. and get first one
    student = Student.select().order_by(Student.points.desc()).get()

    return student
    
if __name__ == '__main__':
    db.connect()
    db.create_tables([Student] ,safe=True) # safe=true to protect db when run the prog multible time
    add_students() 

    print("our top student right now is {0.username}").format(top_student())





