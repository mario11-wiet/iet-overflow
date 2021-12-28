from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q


# Create your views here.
def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')


def home(response):
    q = response.GET.get('q') if response.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count}
    return render(response, 'base/home.html', context)


def room(response, id):
    rooms = Room.objects.get(id=id)
    context = {'rooms': rooms}

    return render(response, 'base/room.html', context)


def createRoom(response):
    form = RoomForm()
    if response.method == 'POST':
        form = RoomForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(response, 'base/room_form.html', context)


def updateRoom(response, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if response.method == "POST":
        form = RoomForm(response.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(response, 'base/room_form.html', context)


def deleteRoom(response, id):
    room = Room.objects.get(id=id)
    if response.method == 'POST':
        room.delete()
        return redirect('home')
    return render(response, 'base/delete.html', {'obj': room})
