from django.shortcuts import redirect
from django.urls import reverse


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'administrator' in request.path:
            if request.session.get('user_type') != 'administrator':
                return redirect(reverse('rateMyUogCourse:login'))
