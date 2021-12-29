from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def okay(response):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')


def loginPage(response):
    page = 'login'

    if response.user.is_authenticated:
        return redirect('home')

    if response.method == "POST":
        username = response.POST.get('username').lower()
        password = response.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(response, 'User does not exist')

        user = authenticate(response, username=username, password=password)

        if user is not None:
            login(response, user)
            return redirect('home')

        else:
            messages.error(response, 'Username or password do not exist')

    context = {'page': page}
    return render(response, 'base/login_register.html', context)


def logoutUser(response):
    logout(response)
    return redirect('home')


def registerPage(response):
    page = 'register'
    form = UserCreationForm()
    if response.method == 'POST':
        form = UserCreationForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(response, user)
            return redirect('home')
        else:
            messages.error(response, "An error occurred during registration")

    return render(response, 'base/login_register.html', {'form': form})


def home(response):
    q = response.GET.get('q') if response.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages':room_messages}
    return render(response, 'base/home.html', context)


def room(response, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if response.method == "POST":
        messages = Message.objects.create(
            user=response.user,
            room=room,
            body=response.POST.get('body')
        )
        room.participants.add(response.user)
        return redirect('room', id=room.id)

    context = {'room': room, 'room_messages': room_messages,'participants':participants}

    return render(response, 'base/room.html', context)


def userProfile(response, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(response, 'base/profile.html',context)

@login_required(login_url='login')
def createRoom(response):
    form = RoomForm()
    if response.method == 'POST':
        form = RoomForm(response.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = response.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(response, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(response, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if response.user != room.host:
        return HttpResponse('Your are not allowed here')

    if response.method == "POST":
        form = RoomForm(response.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(response, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(response, id):
    room = Room.objects.get(id=id)

    if response.user != room.host:
        return HttpResponse('Your are not allowed here')

    if response.method == 'POST':
        room.delete()
        return redirect('home')
    return render(response, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(response, id):
    message = Message.objects.get(id=id)

    if response.user != message.user:
        return HttpResponse('Your are not allowed here')

    if response.method == 'POST':
        message.delete()
        return redirect('home')
    return render(response, 'base/delete.html', {'obj': message})
