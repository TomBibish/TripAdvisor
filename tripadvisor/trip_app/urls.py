from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.index),
    path('signup', views.signup, name='signup'),
    path('logout', auth_views.LogoutView.as_view()),
    path('login', auth_views.LoginView.as_view()),


    path('restaurants', views.restaurants, name='restaurants'),
    path('reviews', views.reviews, name='reviews'),
    path("restaurants/<int:pk>", views.restaurant_details),
    path('restaurants/<int:restaurant_id>/reviews', views.reviews_for_restaurant),

    # path('restaurant/<int:restaurant_id>', views.restaurant_details, name='restaurant_details'),
    path('add_restaurant', views.add_restaurant, name="add_restaurant"),
    path('write_review', views.write_review, name="write_review"),
    path('delete_review/<int:review_id>', views.delete_review, name='delete_review'),
    path('edit_review/<int:review_id>', views.edit_review, name='edit_review'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('write_review_from_restaurant/<int:restaurant_id>', views.write_review_from_restaurant, name='write_review_from_restaurant')
    ]