from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from student.forms import CourseFeedback
from student.models import CourseFeedback as Course_Feedback_Model, StudentFeedbackLikes
from rateMyUogCourse.models import CourseSearchTable
from lecturer.models import Course

def save_feedback(request):
    if request.method == 'POST':
        form = CourseFeedback(request.POST)
        if form.is_valid():
            form.save()
            form_overall = form.cleaned_data['overall'] 
            form_difficulty = form.cleaned_data['difficulty']
            form_usefulness = form.cleaned_data['usefulness']
            form_workload = form.cleaned_data['workload']
            form_would_recommend = form.cleaned_data['would_recommend'] 
            form_professor_rating = form.cleaned_data['professor_rating']
            course_id = form.cleaned_data['courseId']

            count_reviews = Course_Feedback_Model.objects.filter(courseId = course_id).count()

            old_course_overview = CourseSearchTable.objects.filter(courseId = course_id)

            if len(old_course_overview) > 0:

                old_course_overview.overall = (old_course_overview.overall  *  (count_reviews - 1)) + form_overall / count_reviews

                old_course_overview.difficulty = (old_course_overview.difficulty  *  (count_reviews - 1)) + form_difficulty / count_reviews

                old_course_overview.usefulness = (old_course_overview.usefulness  *  (count_reviews - 1)) + form_usefulness / count_reviews

                old_course_overview.workload = (old_course_overview.workload  *  (count_reviews - 1)) + form_workload / count_reviews

                old_course_overview.professorRating = (old_course_overview.professorRating  *  (count_reviews - 1)) + form_professor_rating / count_reviews

                if(form_would_recommend):

                    old_course_overview.wouldRecommend = int(((((old_course_overview.wouldRecommend  *  (count_reviews - 1))/100)+1)  / count_reviews) * 100)
                else:
                    old_course_overview.wouldRecommend = int(((old_course_overview.wouldRecommend  *  (count_reviews - 1)/100)  / count_reviews) * 100)

                old_course_overview.save()

            else:
                 
                course = Course.objects.filter(courseId = course_id)
                 
                courseSearchTableRecord =  CourseSearchTable.objects.create(
                      
                 overall = form_overall,

                 difficulty = form_difficulty,

                 usefulness = form_usefulness,

                 workload = form_workload,

                 professorRating = form_professor_rating,

                 courseName =course.courseName,

                 wouldRecommend = form_would_recommend,

                 courseId = course_id )

                courseSearchTableRecord.save()

            #return redirect('success_url')  # Redirect to a success page
            return HttpResponse('Successful')



def show_detailed_rating(request, course_Id, guId):
    
    context_dict ={}

    detailed_feedback = Course_Feedback_Model.objects.filter(courseId = course_Id)

    context_dict['detailed_feedback'] = detailed_feedback

    overall_course_detail = CourseSearchTable.objects.filter(courseId = course_Id)

    context_dict['overall_course_details'] = overall_course_detail

    feedback_ids = [feedback.feedbackId for feedback in detailed_feedback]

    if(guId != 'None'):
         student_feedback_like_list = StudentFeedbackLikes.objects.filter(guid = guId, feedbackId__in = feedback_ids)

         context_dict['studentFeedbackLike'] = student_feedback_like_list

         context_dict['is_lecturer'] = True

    return render(request, "" , context = context_dict)

def mainPage(request):
 return HttpResponse("Main Page")

 
def register(request):

    # registered = False
    
    # if request.method == 'POST':
    
    #     registration_form = StudentRegistrationForm(request.POST)
        
    #     if registration_form.is_valid():
    #         student = registration_form.save()
            
    #         # not sure about how to confirm password
    #         student.set_password(user.password)
    #         student.save()
            
    #     else:
    #         print(registration_form..errors)
        
    # else:
    #     registration_form = StudentRegistrationForm()
        
    
    return render(request, 'student/mainPage.html', context = {})


def report_feedback(feedback_id):

    try:
        detailed_feedback = Course_Feedback_Model.objects.filter(feedbackId = feedback_id)

        detailed_feedback.reported =  detailed_feedback.reported + 1

        detailed_feedback.save()
   
    except Exception as e:
        print(e)


def like_feedback(feedback_id, guId):

        try:

            detailed_feedback = Course_Feedback_Model.objects.filter(feedbackId = feedback_id)

            detailed_feedback.likes =  detailed_feedback.likes + 1

            detailed_feedback.save()

            studentFeedbackLike = StudentFeedbackLikes.objects.create(guid = guId, feedbackId = feedback_id)

            studentFeedbackLike.save()

        except Exception as e:
            print(e)



def dislike_feedback(feedback_id, guId):
    try:

            detailed_feedback = Course_Feedback_Model.objects.filter(feedbackId = feedback_id)

            detailed_feedback.likes =  detailed_feedback.likes - 1

            detailed_feedback.save()

            studentFeedbackLike = StudentFeedbackLikes.objects.get(guid = guId, feedbackId = feedback_id)

            studentFeedbackLike.delete()

    except Exception as e:
            print(e)


