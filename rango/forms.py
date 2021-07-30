from django import forms
from django.forms import fields
from django.template.defaultfilters import title
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # a class provide additional information on form
    class Meta:
        # provide association between ModelForm and a model, set model attribute to Model used
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.") # max length must equal to the length in data models
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.") # widget for inputting text
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) # entry views and likes and hide widget

    # clean data before store
    def clean(self):
        cleaned_data = self.cleaned_data # obtain from ModelForm dictionary
        url = cleaned_data.get('url') # obtain form's value, if not exists, return none
        
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        model = Page
        # hide foreign key
        exclude = ('category',)