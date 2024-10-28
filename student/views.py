# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from lecturer.models import Course, Lecturer, LecturerCourseAssignment
from rateMyUogCourse.models import CourseSearchTable
from student.forms import CourseFeedback
from student.models import CourseFeedback as Course_Feedback_Model, Student, StudentFeedbackLikes


#Main function, which takes the course feedbacks and save it.
def save_feedback(request, course_id, guId):
    if request.method == 'POST':
        form = CourseFeedback(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Since the form is valid, save the feedback data
            feedback = form.save()

            #Getting the form data for futher calculation
            form_overall = form.cleaned_data['overall']
            form_difficulty = form.cleaned_data['difficulty']
            form_usefulness = form.cleaned_data['usefulness']
            form_workload = form.cleaned_data['workload']
            form_would_recommend = form.cleaned_data['recommendCourse']
            form_professor_rating = form.cleaned_data['lecturerRating']

            #Fetching the query set from the search table for the particular course
            old_course_overview_q = CourseSearchTable.objects.filter(courseId=course_id)

            old_course_overview = old_course_overview_q[0]

            count_reviews = old_course_overview.reviews

            #checking if there was any reviews already existing for the course
            if count_reviews!=0:

                #Calculating the new averages
                old_course_overview.overall = ((old_course_overview.overall * (
                            count_reviews - 1)) + form_overall) / count_reviews

                old_course_overview.difficulty = ((old_course_overview.difficulty * (
                            count_reviews - 1)) + form_difficulty) / count_reviews

                old_course_overview.usefulness = ((old_course_overview.usefulness * (
                            count_reviews - 1)) + form_usefulness) / count_reviews

                old_course_overview.workload = ((old_course_overview.workload * (
                            count_reviews - 1)) + form_workload) / count_reviews

                old_course_overview.professorRating = ((old_course_overview.professorRating * (
                            count_reviews - 1)) + form_professor_rating) / count_reviews

                old_course_overview.reviews = old_course_overview.reviews + 1

                if (form_would_recommend):

                    old_course_overview.wouldRecommend = int(((((old_course_overview.wouldRecommend * (
                                count_reviews - 1)) / 100) + 1) / count_reviews) * 100)
                else:
                    old_course_overview.wouldRecommend = int(
                        ((old_course_overview.wouldRecommend * (count_reviews - 1) / 100) / count_reviews) * 100)

                #save the new row
                old_course_overview.save()

            else:
                #If no reviews were given earlier then add this as the first review
                course_data_search = CourseSearchTable.objects.filter(courseId = course_id)

                search_row = course_data_search[0]

                search_row.overall = form_overall

                search_row.difficulty = form_difficulty

                search_row.usefulness = form_usefulness

                search_row.professorRating = form_professor_rating

                search_row.wouldRecommend = form_would_recommend

                search_row.workload = form_workload

                search_row.reviews = 1

                search_row.save()

            return JsonResponse({'success': True, 'message': 'Course review submitted successfully!'})


# Get the data for the detailed rating page
def show_detailed_rating(request, course_Id, guId):
    context_dict = {}

    #setting the session(could be student or lecturer)
    context_dict['user_type'] = request.session['user_type']
    context_dict['user_id'] = request.session['user_id']
    context_dict['course_id'] = course_Id

    #Get the query set for the course 
    course_query_set = Course.objects.filter(courseId=course_Id)
    context_dict['course_name'] = course_query_set[0].courseName.lower().capitalize()

    context_dict['count_reviews'] = Course_Feedback_Model.objects.filter(courseId=course_Id).count()

    #Fetch the lecturer if for this course
    lecturercourse_query_set = LecturerCourseAssignment.objects.filter(courseId=course_Id)

    lecturer_ids = [item.lecturerId for item in lecturercourse_query_set]

    context_dict['lecturer_query_sets'] = Lecturer.objects.filter(lecturerId__in=lecturer_ids)

    #Fetch the all the feedbacks for the course
    detailed_feedback = Course_Feedback_Model.objects.filter(courseId=course_Id)

    context_dict['detailed_feedback'] = detailed_feedback

    #Get the averages for the particular course
    overall_course_detail = CourseSearchTable.objects.filter(courseId=course_Id)

    context_dict['overall_course_details'] = overall_course_detail[0]

    #Get the feedback ids for which this particular student liked.
    feedback_ids = [feedback.feedbackId for feedback in detailed_feedback]

    if (guId != 'None'):
        feedback_ids_list = list(
            StudentFeedbackLikes.objects.filter(guid=guId, feedbackId__in=feedback_ids).values_list('feedbackId',
                                                                                                    flat=True))

        context_dict['studentFeedbackLike'] = feedback_ids_list

    return render(request, "student/course_detail.html", context=context_dict)


def mainPage(request):
    return HttpResponse("Main Page")


# Reports a feedback and saves it.
def report_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            detailed_feedback = get_object_or_404(Course_Feedback_Model, feedbackId=feedback_id)

            detailed_feedback.reported = detailed_feedback.reported + 1

            detailed_feedback.save()

            return JsonResponse({'reported': True, 'reported_count': detailed_feedback.reported})

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

#Increment the like for a feedback and also adds it in student feedback like table,
#so that the same student shouldnt like the same feedback again.
def like_feedback(request, feedback_id, guId):
    try:
        detailed_feedback = Course_Feedback_Model.objects.get(feedbackId=feedback_id)
        detailed_feedback.likes += 1
        detailed_feedback.save()

        Student.objects.filter(guid=guId)

        studentFeedbackLike = StudentFeedbackLikes.objects.create(guid=Student.objects.get(guid=guId),
                                                                  feedbackId=detailed_feedback)
        studentFeedbackLike.save()

        return JsonResponse({'success': True})  # Return a success response
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)  # Return an error response with status 500


