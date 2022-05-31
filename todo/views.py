from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import InviteForm
from .models import Invite
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_invites')
            except IntegrityError:
                return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('current_invites')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_invite(request):
    if request.method == 'GET':
        return render(request, 'todo/create_invite.html', {'form': InviteForm()})
    else:
        try:
            form = InviteForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_invites')
        except ValueError:
            return render(request, 'todo/create_invite.html', {'form': InviteForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def current_invites(request):
    invites = Invite.objects.filter(
        user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/current_invites.html', {'invites': invites})


@login_required
def completed_invites(request):
    invites = Invite.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completed_invites.html', {'invites': invites})


@login_required
def view_invites(request, todo_pk):
    invites = get_object_or_404(Invite, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = InviteForm(instance=Invite)
        return render(request, 'todo/view_invites.html', {'invites': Invite, 'form': form})
    else:
        try:
            form = InviteForm(request.POST, instance=invites)
            form.save()
            return redirect('current_invites')
        except ValueError:
            return render(request, 'todo/view_invites.html', {'invites': invites, 'form': form, 'error': 'Bad info'})


@login_required
def complete_invite(request, todo_pk):
    invite = get_object_or_404(Invite, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        invite.datecompleted = timezone.now()
        invite.save()
        return redirect('current_invites')


@login_required
def delete_invite(request, todo_pk):
    invite = get_object_or_404(Invite, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        invite.delete()
        return redirect('current_invites')
