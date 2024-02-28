import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rate_my_uog_course.settings')

import django
django.setup()
from student.models import Student, CourseFeedback, StudentFeedbackLikes
from lecturer.models import Lecturer, Course, LecturerCourseAssignment
from rateMyUogCourse.models import CourseSearchTable, WebsiteFeedback
from administrator.models import Admin

def populate():
   
    # dummy data for Student

    students = [
        {'guid': '1234567',
         'email': '1234567t@student.gla.ac.uk',
         'name': 'test_user_1',
         'password': '1qaz@WSX',
         'programType': 'CS'},
        {'guid': '7654321',
         'email': '7654321t@student.gla.ac.uk',
         'name': 'test_user_2',
         'password': '!QAZ2wsx',
         'programType': 'IT'} ]
         
    for student in students:
        s = add_student(student['guid'], student['email'], student['name'], student['password'], student['programType'])
    
    # dummy data for Course
    courses = [
        {'courseId': 'COMPSCI4039',
         'courseName': 'PROGRAMMING',
         'programType': 'IT+',
         'semester': 1},
        {'courseId': 'COMPSCI4084',
         'courseName': 'PROGRAMMING AND SYSTEMS DEVELOPMENT (H)',
         'programType': 'CS+',
         'semester': 1},
        {'courseId': 'COMPSCI5004',
         'courseName': 'ALGORITHMS AND DATA STRUCTURES (M)',
         'programType': 'IT+',
         'semester': 2},
    ]
    for course in courses:
        c = add_course(course['courseId'], course['courseName'], course['programType'], course['semester'])
        
    # dummy data for CourseFeedback
    courseFeedbacks = [
        {'courseId': 'COMPSCI4039',
         'guid': '1234567',
         'overall': 7,
         'difficulty': 6,
         'usefulness': 6,
         'workload': 5,
         'examFormat': 'test',
         'evaluationMethod': 'some text here',
         'lecturerRating': 5,
         'gradeReceived': 'A3',
         'recommendCourse': True,
         'textFeedback': 'dummy data for course feedback...'}
    ]
    f = add_courseFeedback(courseFeedbacks[0])
    
    # calculate for courseSearchTable
    cal_courseSearchTable(courseFeedbacks[0]['courseId'])
    
    # dummy data for Lecturer

    lecturer = [
        {'lecturerId': 'test.lecturer',
         'lecturerName': 'test lecturer',
         'designation': 'prof.',
         'password': '1qaz@WSX3edc'
        }
    ]
    l = add_lecturer(lecturer[0]['lecturerId'], lecturer[0]['lecturerName'], lecturer[0]['designation'], lecturer[0]['password'])
    
    # dummy data for LecturerCourseAssignment
    
    LecturerCourseAssignment.objects.create(lecturerId = Lecturer.objects.get(lecturerId = 'test.lecturer'), courseId = Course.objects.get(courseId = 'COMPSCI4039'))
    
    # dummy data for WebsiteFeedback
    
    websiteFeedback = {'friendly': 9, 'overall': 9, 'aesthetic': 8, 'comment': 'dummy data for websiteFeedback!'}
    
    websiteFeedback = WebsiteFeedback.objects.create(friendly = websiteFeedback['friendly'], overall = websiteFeedback['overall'],
    aesthetic = websiteFeedback['aesthetic'], comment = websiteFeedback['comment'])
    
    # Admin user
    admin = {'userName': 'administrator', 'password': '1qaz@WSX'}
    Admin.objects.create(userName = admin['userName'], password = admin['password'])
            
def add_student(guid, email, name, password, program):
    s = Student.objects.get_or_create(guid = guid)[0]
    s.email = email
    s.name = name
    s.password = password
    s.programType = program
    s.save()
    return s
    
def add_course(cid, name, program, s):
    c = Course.objects.get_or_create(courseId = cid, semester = s)[0]
    c.courseName = name
    c.programType = program
    # c.semester = s
    c.save()
    return c
    
def add_courseFeedback(feedback):
    f = CourseFeedback.objects.create(courseId = Course.objects.get(courseId = feedback['courseId']), guid = Student.objects.get(guid = feedback['guid']), 
    overall = feedback['overall'], difficulty = feedback['difficulty'], usefulness = feedback['usefulness'], workload = feedback['workload'], 
    examFormat = feedback['examFormat'],evaluationMethod = feedback['evaluationMethod'], lecturerRating = feedback['lecturerRating'],
    gradeReceived = feedback['gradeReceived'], recommendCourse = feedback['recommendCourse'], textFeedback = feedback['textFeedback'])
    f.save()
    return f
    
def add_lecturer(lid, name, d, password):
    l = Lecturer.objects.get_or_create(lecturerId = lid)[0]
    l.lecturerName = name
    l.designation = d
    l.password = password
    return l
def cal_courseSearchTable(cid):
    course_data = CourseFeedback.objects.filter(courseId = cid)
    overall, difficulty, usefulness, workload, reviews, wouldRecommend = 0,0,0,0,0,0
    for row in course_data:
        overall += row.overall
        difficulty += row.difficulty
        usefulness += row.usefulness
        workload += row.workload
        reviews+=1
        if row.recommendCourse == True:
            wouldRecommend+=1 
    overall = overall/course_data.count()
    difficulty = difficulty/course_data.count()
    usefulness = usefulness/course_data.count()
    workload = workload/course_data.count()
    wouldRecommend = round(wouldRecommend/course_data.count(),2)
    
    r = CourseSearchTable.objects.create(courseId = Course.objects.get(courseId = cid), courseName = Course.objects.get(courseId = cid).courseName, 
    overall = overall, difficulty = difficulty, usefulness = usefulness, workload = workload, reviews = reviews, wouldRecommend = wouldRecommend)
       

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

    