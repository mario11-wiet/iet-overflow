from math import ceil

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

room_on_page = 5


# Create your views here.
def okay(response):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')


def loginPage(response):
    page = 'login'

    if response.user.is_authenticated:
        return redirect('home')

    if response.method == "POST":
        email = response.POST.get('email').lower()
        password = response.POST.get('password')

        try:
            User.objects.get(email=email)
        except:
            messages.error(response, 'User does not exist')

        user = authenticate(response, email=email, password=password)

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
    form = MyUserCreationForm()
    if response.method == 'POST':
        form = MyUserCreationForm(response.POST)
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
    page = int(response.GET.get('page') if response.GET.get('page') is not None else 1)
    if response.GET.get('qSearch') is not None:
        q = response.GET.get('qSearch')
        rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))

    elif response.GET.get('q') is not None:
        q = response.GET.get('q')
        rooms = Room.objects.filter(Q(topic__name__icontains=q))

    else:
        q = ''
        rooms = Room.objects.all()

    room_count = rooms.count()
    page_number = [i for i in
                   range(page - 2 if page > 2 else page - 1 if page > 1 else 1,
                         min((page + 3 if page > 2 else page + 4 if page > 1 else page + 5),
                             (ceil(rooms.count() / room_on_page)) + 1))]
    page_number.remove(1) if 1 in page_number else None
    rooms = rooms[(page - 1) * room_on_page:((page - 1) * room_on_page) + room_on_page]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
    topics = Topic.objects.all()[0:5]

    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages,
               'page_number': page_number}
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

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}

    return render(response, 'base/room.html', context)


def userProfile(response, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(response, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(response):
    form = RoomForm()
    topics = Topic.objects.all()
    if response.method == 'POST':
        topic_name = response.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=response.user,
            topic=topic,
            name=response.POST.get('name'),
            description=response.POST.get('description'),
        ).participants.add(response.user)
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(response, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(response, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if response.user != room.host:
        return HttpResponse('Your are not allowed here')

    if response.method == "POST":
        topic_name = response.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = response.POST.get('name')
        room.topic = topic
        room.description = response.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
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


@login_required(login_url='login')
def updateUser(response):
    user = response.user
    form = UserForm(instance=user)

    if response.method == "POST":
        form = UserForm(response.POST, response.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', id=user.id)
    context = {'form': form}
    return render(response, 'base/update-user.html', context)


def topicsPage(response):
    q = response.GET.get('q') if response.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(response, 'base/topics.html', context)


def activityPage(response):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(response, 'base/activity.html', context)
