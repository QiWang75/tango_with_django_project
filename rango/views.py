from django.shortcuts import render

# Create your views here.
# import httpresponse object from http module
from django.http import HttpResponse

# create index view
# each view has at least 1 argument and must return httpresponse object
def index(request):
    return HttpResponse("Rango says hey there parter!")