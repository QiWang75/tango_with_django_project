# import URL mapping and views module
from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    # create path(string to match, view called if matched, reference of view by naming) function
    path('', views.index, name='index'), #call url and point to index view for mapping
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
]
