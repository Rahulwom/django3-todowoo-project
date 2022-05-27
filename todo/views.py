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

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentinvites')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentinvites')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createinvite(request):
    if request.method == 'GET':
        return render(request, 'todo/createinvite.html', {'form':InviteForm()})
    else:
        try:
            form = InviteForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentinvites')
        except ValueError:
            return render(request, 'todo/createinvite.html', {'form':InviteForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def currentinvites(request):
    invites = Invite.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currentinvites.html', {'invites':invites})

@login_required
def completedinvites(request):
    invites = Invite.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedinvites.html', {'invites':invites})

@login_required
def viewinvites(request, todo_pk):
    invites = get_object_or_404(Invite, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = InviteForm(instance=Invite)
        return render(request, 'todo/viewinvites.html', {'invites':Invite, 'form':form})
    else:
        try:
            form = InviteForm(request.POST, instance=invites)
            form.save()
            return redirect('currentinvites')
        except ValueError:
            return render(request, 'todo/viewinvites.html', {'invites':invites, 'form':form, 'error':'Bad info'})

@login_required
def completeinvite(request, todo_pk):
    invite = get_object_or_404(Invite, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        invite.datecompleted = timezone.now()
        invite.save()
        return redirect('currentinvites')

@login_required
def deleteinvite(request, todo_pk):
    invite = get_object_or_404(Invite, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        invite.delete()
        return redirect('currentinvites')
