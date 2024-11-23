from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView,DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Review
from .forms import ReviewForm

# Create your views here.
def home(request):
    return render(request, "index.html",)

def about(request):
    about_content = {'about':"SmallScapes is a landscaping company based in Indiana."}
    return render(request, "about.html", {'content':about_content})

def projects(request):
    return render(request, "projects.html",)

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_thanks')

class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'



class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

class ReviewThanksView(TemplateView):
    template_name = 'thank_you.html'
