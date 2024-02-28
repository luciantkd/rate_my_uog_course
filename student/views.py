from django.shortcuts import render
from student.forms import StudentRegistrationForm
# Create your views here.
from django.http import HttpResponse
from student.forms import CourseFeedback
from student.models import CourseFeedback as Course_Feedback_Model
from rateMyUogCourse.models import CourseSearchTable

def get_feedback(request):
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

            #return redirect('success_url')  # Redirect to a success page
            return HttpResponse('Successful')



def show_detailed_rating(request, course_Id):
    
    context_dict ={}

    detailed_feedback = Course_Feedback_Model.objects.filter(courseId = course_Id)

    context_dict['detailed_feedback'] = detailed_feedback

    overall_course_detail = CourseSearchTable.objects.filter(courseId = course_Id)

    context_dict['overall_course_details'] = overall_course_detail

    return render(request, "", context = context_dict)

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
