from django import forms
from django.forms import Select, Textarea, TextInput, DateInput, HiddenInput

from .models import *


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    type = forms.ModelChoiceField(queryset=RestaurantType.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    price_range = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    image = forms.URLField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Restaurant
        fields = ['name', 'country', 'city', 'address', 'type', 'price_range', 'image']


class MyDateWidget(DateInput):
    input_type = 'date'


class ReviewForm(forms.ModelForm):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(),
                                        widget=Select(attrs={'class': 'form-control'}))
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  widget=HiddenInput(attrs={'class': 'form-control'}))
    stars = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    review_title = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    review_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    visit_date = forms.DateField(widget=MyDateWidget())

    class Meta:
        model = Review
        fields = ['restaurant', 'user', 'stars', 'review_title', 'review_text', 'visit_date']


class ReviewFormEdit(ReviewForm):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(),
                                        widget=HiddenInput(attrs={'class': 'form-control'}))


class UserProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  widget=HiddenInput(attrs={'class': 'form-control'}))
    image = forms.URLField(widget=TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(widget=MyDateWidget())
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['user', 'image', 'birth_date', 'country', 'city', 'address']
