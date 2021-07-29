from django.shortcuts import render

# Create your views here.
# import httpresponse object from http module
from django.http import HttpResponse

# create index view
# each view has at least 1 argument and must return httpresponse object
def index(request):
    # construct a dictionary as content to pass to template, key matches to template
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # return a rendered response: render(input, template filename, context dictionary)
    return render(request, 'rango/index.html', context=context_dict)

# create about view
def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
