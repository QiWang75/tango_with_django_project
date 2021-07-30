# import httpresponse object from http module
from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# import Category model
from rango.models import Category
# import Page model
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm

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

def register(request):
    # boolean, if registration is successful, true when succeeds
    registered = False

    if request.method =='POST':
        # grab information from form
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # hash password and update user
            user.set_password(user.password)
            user.save()

            # sort out user profile
            profile = profile_form.save(commit=False) # delay saving to avoid integrity problems
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] # get profile picture from form to model

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm() # blank form ready to input

    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # gather from form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if name and password valid, return user object
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
