from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# Create your views here.
def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')


def home(response):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(response, 'base/home.html', context)


def room(response, id):
    rooms = Room.objects.get(id=id)
    context = {'rooms': rooms}

    return render(response, 'base/room.html', context)


def createRoom(response):
    context = {}
    return render(response,'base/room_form.html', context)