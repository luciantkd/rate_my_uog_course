from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def mainPage(request):
 return HttpResponse("Main Page")


def login(request):
 return HttpResponse("login")
