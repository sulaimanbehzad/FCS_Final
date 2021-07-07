import os

from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http.request  import HttpRequest

from . import models

import subprocess
import sys

from .models import UserAccessInformationModel


def login(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'registration/linux-login.html')
    elif request.method == 'POST':
        metaa = request.META
        headerrs = request.headers

        username = request.POST['username']
        passwd = request.POST['passwd']
        
        host_name = metaa['REMOTE_HOST']
        method = metaa['REQUEST_METHOD']
        server_name = metaa['SERVER_NAME']

        
        accept_encoding = headerrs.get("Accept-Encoding")
        content_encoding = headerrs.get("Content-Encoding")
        user_email = headerrs.get("From")
        user_agent = headerrs.get("User-Agent")
        cookie = headerrs.get("Cookie")
        origin_date = headerrs.get("Date")
        content_length = headerrs.get("Content-Length")
        host_ = headerrs.get("Host")

        
        cmd1 = f"""openssl passwd -6 -salt $( sudo cat /etc/shadow | grep "^{username}:.*$" | cut -d'$' -f3 ) {passwd} | cut -d'$' -f4"""
        user_input = subprocess.run(cmd1, shell=True, capture_output=True, text=True,)
        print(f'{user_input}')
        cmd2 = f"""sudo cat /etc/shadow | grep "^{username}:.*$" | cut -d'$' -f4 | cut -d':' -f1"""
        the_hash = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
        
        request_data = models.UserAccessInformationModel(
            username=username, passwd=user_input, tried_at=origin_date,
            host=host_, method=method, user_email=user_email, cookie=cookie,
            server_name=server_name, content_encoding=content_encoding,
            accept_encoding=accept_encoding, content_length=int(content_length),
        )

        request_data.save()


        print(f'{the_hash}')
        if the_hash.stdout == user_input.stdout:
            request.session.set_expiry(86400)
            request.session['username'] = username
            return render(request, 'home/home.html')
        else:
            return render(request, 'registration/linux-login.html')
    

def viewFiles(request):
    if request.method=="GET":
        username = None
        print(f'{request}')
        if request.session['username'] != None:
            print('authenticated')
            username = request.session['username']
            print(username)
            os.chdir('files/')
            cmd2= f"""ls -l | grep {username}"""
            output = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
            print(f'{output.stdout}')
            context={'files_list': output.stdout}
            return render(request, 'fileViewer/files.html', context)
        else:
            return render(request, 'registration/linux-login.html')
    else:
        return render(request, 'registration/linux-login.html')

def getFrequents(request):
    if request.method == "GET":
        mc_user = UserAccessInformationModel.objects.values("username").annotate(count=Count('username')).order_by("-count")
        print(type(mc_user))
        print(f'MOST COMMON USER NAME: \n {mc_user[0]}')
        mc_pass = UserAccessInformationModel.objects.values("passwd").annotate(count=Count('passwd')).order_by("-count")
        print(f'MOST COMMON PASSOORD: \n {mc_pass[0]}')
        most_commons = {'most_common_username': mc_user[0], 'most_common_password': mc_pass[0]}
        return render(request, 'mostCommon.html', most_commons)
    else:
        return render(request, 'registration/linux-login.html')
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('/')
#         else:
#             return render(request, 'signup.html', {'form': form})
#     else:
#         form = UserCreationForm()
#         return render(request, 'signup.html', {'form': form})
#
# def signin(request):
#     if request.user.is_authenticated:
#         return render(request, 'homepage.html')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             form = AuthenticationForm(request.POST)
#             return render(request, 'login.html', {'form': form})
#     else:
#         form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})
#
# def signout(request):
#     logout(request)
#     return redirect('/')
