from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')



def home(response):
    return render(response, 'base/home.html', {})


def room(response):
    return render(response, 'room.html', {})
