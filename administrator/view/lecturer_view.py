from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse

from lecturer.models import Lecturer
from rateMyUogCourse.views import encryptPassword
from django.contrib import messages


def lecturer_management(request):
    # Retrieve the search query from the request's GET parameters
    search_query = request.GET.get('query', '')

    # If a search query is provided, filter lecturers based on the query present in their name or email
    if search_query:
        lecturers = Lecturer.objects.filter(
            Q(lecturerName__icontains=search_query) |
            Q(email__icontains=search_query)
        ).values('lecturerId', 'lecturerName', 'designation', 'email').order_by('lecturerId')
    else:
        # If no search query, retrieve all lecturers
        lecturers = Lecturer.objects.all().values('lecturerId', 'lecturerName', 'designation', 'email').order_by('lecturerId')

    # Render and return the lecturer management template, passing the lecturers queryset
    return render(request, 'administrator/lecturer_management.html', {'lecturers': lecturers})

def lecturer_edit(request):
    # Attempt to retrieve the lecturer ID from the request's GET parameters
    lecturer_id = request.GET.get('lecturer_id')
    if request.method == 'POST':
        # Extract and clean form data from POST request
        lecturer_id = request.POST.get('lecturerId', '').strip()
        lecturer_name = request.POST.get('lecturerName', '').strip()
        designation = request.POST.get('designation', '').strip()
        email = request.POST.get('Email', '').strip()
        password = request.POST.get('Password', '').strip()

        # Validate that required fields are not empty
        if not all([lecturer_name, designation, email]):
            messages.error(request, "Name, designation, and email cannot be empty.")
            return render(request, 'administrator/lecturer_edit.html', {
                'lecturer_entity': {
                    'lecturerId': lecturer_id,
                    'lecturerName': lecturer_name,
                    'designation': designation,
                    'email': email,
                }
            })

        # Handle both editing an existing lecturer and adding a new one
        if lecturer_id:
            lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
        else:
            if not password:
                messages.error(request, "Password cannot be empty.")
                return render(request, 'administrator/lecturer_edit.html', {
                    'lecturer_entity': {
                        'lecturerId': lecturer_id,
                        'lecturerName': lecturer_name,
                        'designation': designation,
                        'email': email,
                    }
                })

            lecturer_id = email.split('@')[0]  # Logic for generating lecturer ID
            # Convert lecturer ID to lowercase
            lecturer_id = lecturer_id.lower()
            lecturer = Lecturer(lecturerId=lecturer_id)

        # Update lecturer attributes
        lecturer.lecturerName = lecturer_name
        lecturer.designation = designation
        lecturer.email = email

        # If a password is provided, encrypt and update it
        if password:
            lecturer.password = encryptPassword(password)

        # Save the lecturer to the database
        lecturer.save()

        # Redirect to the lecturer management page after saving
        return redirect(reverse('administrator:lecturer_management'))

    else:  # Handle GET request for the edit page
        lecturer_entity = {}
        if lecturer_id:
            # If editing an existing lecturer, fetch their details
            lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
            lecturer_entity = {
                'lecturerId': lecturer.lecturerId,
                'lecturerName': lecturer.lecturerName,
                'designation': lecturer.designation,
                'email': lecturer.email
            }
        # Render and return the lecturer edit template
        return render(request, 'administrator/lecturer_edit.html', {'lecturer_entity': lecturer_entity})

def lecturer_delete(request):
    if request.method == "POST":
        # Retrieve lecturer ID from POST request and delete the specified lecturer
        lecturer_id = request.POST.get('lecturer_id')
        lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
        lecturer.delete()
        # Redirect to the lecturer management page after deletion
        return redirect(reverse('administrator:lecturer_management'))
    else:
        # If not a POST request, redirect to the lecturer management page
        return redirect(reverse('administrator:lecturer_management'))