from django.shortcuts import render

# Create your views here.
def home(request):
    """首页视图"""
    return render(request, 'home.html')
