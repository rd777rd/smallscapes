from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('projects', views.projects, name='projects'),
    path('reviews', views.review_list, name='review_list'),
    path('reviews/leave', views.leave_review, name='leave_review'),
    path('reviews/thank-you', views.thank_you, name='thank_you'),
    path('reviews/delete/<int:id>', views.delete_review, name='delete_review'),
]
