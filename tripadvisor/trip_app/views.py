import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import RestaurantForm, ReviewForm, ReviewFormEdit, UserProfileForm
from .models import *

# Create your views here.
from django.db.models import Q, Count
from django.template.defaulttags import register
from django.core import serializers

from .serializers import RestaurantSerializer, ReviewSerializer


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@api_view(['GET', 'POST'])
def restaurants(request):
    if request.method == 'GET':
        all_restaurants = Restaurant.objects.all()
        if 'country' in request.GET and request.GET['country']:
            all_restaurants = all_restaurants.filter(country__name__icontains=request.GET['country'])
        if 'name' in request.GET and request.GET['name']:
            all_restaurants = all_restaurants.filter(name__icontains=request.GET['name'])
        if 'city' in request.GET and request.GET['city']:
            all_restaurants = all_restaurants.filter(city__city__icontains=request.GET['city'])
        if 'type' in request.GET and request.GET['type']:
            all_restaurants = all_restaurants.filter(type__name__icontains=request.GET['type'])
        if 'sort_by_reviews' in request.GET:
            if request.GET['sort_by_reviews'] == "desc":
               all_restaurants = Restaurant.objects.annotate(total=Count('review')).order_by('-total')
            elif request.GET['sort_by_reviews'] == "asc":
               all_restaurants = Restaurant.objects.annotate(total=Count('review')).order_by('total')

        serializer = RestaurantSerializer(all_restaurants, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def restaurant_details(request, pk):
    try:
        rest = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RestaurantSerializer(rest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RestaurantSerializer(rest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def reviews(request):
    if request.method == 'GET':
        all_reviews = Review.objects.all()
        serializer = ReviewSerializer(all_reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def reviews_for_restaurant(request, restaurant_id):
    try:
        review = Review.objects.filter(restaurant_id=restaurant_id)
        if 'user' in request.GET and request.GET['user']:
            review = review.filter(user__id__icontains=request.GET['user'])
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    restaurant_query_set = Restaurant.objects.all()
    if 'filter_restaurant' in request.GET and request.GET['filter_restaurant']:
        restaurant_query_set = restaurant_query_set.filter(Q(city__city__icontains=request.GET['filter_restaurant']) |
                                                        Q(country__name__icontains=request.GET['filter_restaurant']) |
                                                        Q(name__icontains=request.GET['filter_restaurant']))
    if 'sort_by_price' in request.GET:
        if request.GET['sort_by_price'] == "desc":
            restaurant_query_set = restaurant_query_set.order_by('price_range')
        else:
            restaurant_query_set = restaurant_query_set.order_by('-price_range')
    restaurant_list = [restaurant for restaurant in restaurant_query_set]
    reviews_query_set = Review.objects.all()
    reviews_list = [review for review in reviews_query_set]
    reviews_dict = {}
    stars_dict = {}
    int_start_dict = {}
    for review in reviews_list:
        if review.restaurant.name in reviews_dict.keys():
            reviews_dict[review.restaurant.name].append(review)
            stars_dict[review.restaurant.name].append(float(review.stars))
        else:
            reviews_dict[review.restaurant.name] = [review]
            stars_dict[review.restaurant.name] = [float(review.stars)]
    for restaurant_stars in stars_dict:
        stars_dict[restaurant_stars] = sum(stars_dict[restaurant_stars]) / len(stars_dict[restaurant_stars])
        int_start_dict[restaurant_stars] = range(int(stars_dict[restaurant_stars]))

    return render(request=request,
                  template_name='trip_app/index.html',
                  context={'restaurants': restaurant_list,
                           'reviews': reviews_dict,
                           'int_stars': int_start_dict}
                  )


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'trip_app/signup.html', {'form': form})


# @login_required
# def restaurant_details(request, restaurant_id):
#     restaurant = Restaurant.objects.get(pk=restaurant_id)
#     reviews_query_set = Review.objects.all()
#     reviews_query_set = reviews_query_set.filter(restaurant=restaurant)
#     reviews_list = [review for review in reviews_query_set]
#     stars = {}
#     for review in reviews_list:
#         stars[review.id] = range(int(review.stars))
#     return render(request=request,
#                   template_name='trip_app/restaurant_details.html',
#                   context={'restaurant': restaurant,
#                            'reviews': reviews_list,
#                            'stars': stars})


@login_required
def add_restaurant(request):
    if request.method == 'GET':
        form = RestaurantForm()
        return render(request, template_name='trip_app/add_restaurant.html', context={'form': form})
    elif request.method == 'POST':
        form = RestaurantForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, template_name='trip_app/add_restaurant.html', context={'form': form})


@login_required
def write_review(request):
    if request.method == 'GET':
        form = ReviewForm(initial={'user': request.user})
        return render(request, template_name='trip_app/write_review.html', context={'form': form})
    elif request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, template_name='trip_app/write_review.html', context={'form': form})


@login_required
def write_review_from_restaurant(request,restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    if request.method == 'GET':
        form = ReviewFormEdit(initial={'user': request.user,
                                       'restaurant': restaurant})
        return render(request, template_name='trip_app/write_review.html', context={'form': form})
    elif request.method == 'POST':
        form = ReviewFormEdit(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, template_name='trip_app/write_review.html', context={'form': form})


@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        review.delete()
        return redirect('/')
    return render(request, template_name='trip_app/delete_review.html', context={'review': review})


@login_required
def edit_review(request, review_id):
    review = Review.objects.get(pk=review_id)
    if request.method == "POST":
        form = ReviewFormEdit(instance=review, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        return render(request, template_name="trip_app/edit_review.html",
                      context={"form": ReviewFormEdit(instance=review),
                               "review": review})


@login_required
def user_profile(request, user_id):
    reviews_query_set = Review.objects.all()
    reviews_query_set = reviews_query_set.filter(user=user_id)
    reviews_list = [review for review in reviews_query_set]
    has_profile = False
    all_users = UserProfile.objects.all()
    all_users_list = [user for user in all_users]
    for user in all_users_list:
        if user.id == user_id:
            user_profile = UserProfile.objects.get(pk=user_id)
            has_profile = True
            break
    if request.method == 'GET':
        if has_profile:
            form = UserProfileForm(initial={'user': request.user}, instance=user_profile)
        else:
            form = UserProfileForm(initial={'user': request.user})
        return render(request, template_name='trip_app/user_profile.html', context={'form': form,
                                                                                    'reviews':reviews_list})
    elif request.method == 'POST':
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, template_name='trip_app/user_profile.html', context={'form': form})
