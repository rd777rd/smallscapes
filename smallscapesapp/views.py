from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, "index.html",)

def about(request):
    about_content = {'about':"SmallScapes is a landscaping company based in Indiana."}
    return render(request, "about.html", {'content':about_content})

def projects(request):
    return render(request, "projects.html",)