from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect, render
from django.urls import reverse

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
    page_list = Page.objects.order_by('-views')[:5]

    # place list in dictionary that will be passed to template
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

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
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            # save new category ti database
            form.save(commit=True)
            # confirm and redirect user back to index view
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
