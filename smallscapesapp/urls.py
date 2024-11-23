from django.urls import path
from . import views
from .views import ReviewCreateView, ReviewListView,ReviewDeleteView, ReviewThanksView

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('projects/', views.projects, name="projects"),
    path('leave-review/', ReviewCreateView.as_view(), name='leave_review'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/delete/<int:pk>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('thanks/', ReviewThanksView.as_view(), name='review_thanks'),
    
]