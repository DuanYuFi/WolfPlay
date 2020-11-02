"""backend URL Configuration

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
from django.urls import path, include
from play.views import Register, Login, Logout, test
from play.chats import sendMessage, getRoomMembers, createRoom, joinRoom, leaveRoom

base_URL = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('play/', include('play.urls')),
    path('%suser/register/' % base_URL, Register, name="Register"),
    path('%suser/login/' % base_URL, Login, name="Login"),
    path('%suser/logout/' % base_URL, Logout, name="Logout"),
    path('%suser/test/' % base_URL, test, name = "test"),
    path('%schat/sendmessage/' % base_URL, sendMessage, name = "sendMessage"),
    path('%schat/getroommembers/' % base_URL, getRoomMembers, name = "getRoomMembers"),
    path('%schat/createroom/' % base_URL, createRoom, name = "createRoom"),
    path('%schat/joinroom/' % base_URL, joinRoom, name = "joinRoom"),
    path('%schat/leaveroom/' % base_URL, leaveRoom, name = "leaveRoom")

]
