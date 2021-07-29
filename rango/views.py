from django.shortcuts import render

# Create your views here.
# import httpresponse object from http module
from django.http import HttpResponse

# import Category model
from rango.models import Category
# import Page model
from rango.models import Page

# create index view
# each view has at least 1 argument and must return httpresponse object
def index(request):
    # query database for a list of stored categories
    # order categories by likes in descending order and retrieve subset including top 5
    category_list = Category.objects.order_by('-likes')[:5]

    # place list in dictionary that will be passed to template
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # return a rendered response: render(input, template filename, context dictionary)
    return render(request, 'rango/index.html', context=context_dict)

# create about view
def about(request):
    return render(request, 'rango/about.html')

# create showcategory view
def show_category(request, category_name_slug):
    #create a content dictionary which pass to template rendering engine
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug) # return one model / raise an DoesNotExist exception
        pages = Page.objects.filter(category=category) # retrieve associated pages, empty or a list

        # add pages list to template context under name pages
        context_dict['pages'] = pages
        # add category from database to context dictionary and verify if exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)
