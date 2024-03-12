from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from student.forms import CourseFeedback
from student.models import CourseFeedback as Course_Feedback_Model, StudentFeedbackLikes
from rateMyUogCourse.models import CourseSearchTable
from lecturer.models import Course, Lecturer, LecturerCourseAssignment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def save_feedback(request,course_id, guId):
    if request.method == 'POST':
        form = CourseFeedback(request.POST)
        print(form)

        for field_name, field_value in form.cleaned_data.items():
                print(f"{field_name}: {field_value}")
        print(form.errors)

        # Check if the form is valid
        if form.is_valid():
            # Since the form is valid, save the feedback data
            feedback = form.save()
            form_overall = form.cleaned_data['overall'] 
            form_difficulty = form.cleaned_data['difficulty']
            form_usefulness = form.cleaned_data['usefulness']
            form_workload = form.cleaned_data['workload']
            form_would_recommend = form.cleaned_data['recommendCourse'] 
            form_professor_rating = form.cleaned_data['lecturerRating']


            old_course_overview_m = CourseSearchTable.objects.filter(courseId = course_id)

            old_course_overview=old_course_overview_m[0]

            count_reviews = old_course_overview.reviews

            if old_course_overview:

                print(old_course_overview.overall, count_reviews)

                old_course_overview.overall = ((old_course_overview.overall  *  (count_reviews - 1)) + form_overall )/ count_reviews

                print(old_course_overview.overall)

                old_course_overview.difficulty = ((old_course_overview.difficulty  *  (count_reviews - 1)) + form_difficulty) / count_reviews

                old_course_overview.usefulness = ((old_course_overview.usefulness  *  (count_reviews - 1)) + form_usefulness) / count_reviews

                old_course_overview.workload = ((old_course_overview.workload  *  (count_reviews - 1)) + form_workload) / count_reviews

                old_course_overview.professorRating = ((old_course_overview.professorRating  *  (count_reviews - 1)) + form_professor_rating )/ count_reviews

                old_course_overview.reviews = old_course_overview.reviews + 1

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
            # return HttpResponse('Successful')
            return JsonResponse({'success': True, 'message': 'Course review submitted successfully!'})



def show_detailed_rating(request, course_Id, guId):
    
    context_dict ={}

    context_dict['user_type'] = request.session['user_type']
    context_dict['user_id'] = request.session['user_id']
    context_dict['course_id'] = course_Id

    course_query_set = Course.objects.filter(courseId = course_Id)
    context_dict['course_name'] = course_query_set[0].courseName.lower().capitalize()

    context_dict['count_reviews'] = Course_Feedback_Model.objects.filter(courseId = course_Id).count()

    lecturercourse_query_set = LecturerCourseAssignment.objects.filter(courseId = course_Id)

    lecturer_ids = [item.lecturerId for item in lecturercourse_query_set]

    context_dict['lecturer_query_sets'] = Lecturer.objects.filter(lecturerId__in=lecturer_ids)


    print(context_dict['lecturer_query_sets'])

    detailed_feedback = Course_Feedback_Model.objects.filter(courseId = course_Id)

    context_dict['detailed_feedback'] = detailed_feedback

    overall_course_detail = CourseSearchTable.objects.filter(courseId = course_Id)

    context_dict['overall_course_details'] = overall_course_detail[0]

    feedback_ids = [feedback.feedbackId for feedback in detailed_feedback]

    if(guId != 'None'):
         student_feedback_like_list = StudentFeedbackLikes.objects.filter(guid = guId, feedbackId__in = feedback_ids)

         context_dict['studentFeedbackLike'] = student_feedback_like_list

         context_dict['is_lecturer'] = True

    return render(request, "student/course_detail.html" , context = context_dict)

def mainPage(request):
 return HttpResponse("Main Page")



def report_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            # detailed_feedback = Course_Feedback_Model.objects.filter(feedbackId = feedback_id)
            detailed_feedback = get_object_or_404(Course_Feedback_Model, feedbackId=feedback_id)

            detailed_feedback.reported =  detailed_feedback.reported + 1

            detailed_feedback.save()

            return JsonResponse({'reported': True, 'reported_count': detailed_feedback.reported})
    
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


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


