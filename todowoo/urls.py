"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signup_user, name='signup_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # Todos
    path('', views.home, name='home'),
    path('create/', views.create_invite, name='create_invite'),
    path('current/', views.current_invites, name='current_invites'),
    path('completed/', views.completed_invites, name='completed_invites'),
    path('todo/<int:todo_pk>', views.view_invites, name='view_invites'),
    path('todo/<int:todo_pk>/complete', views.complete_invite, name='complete_invite'),
    path('todo/<int:todo_pk>/delete', views.delete_invite, name='delete_invite'),
]
