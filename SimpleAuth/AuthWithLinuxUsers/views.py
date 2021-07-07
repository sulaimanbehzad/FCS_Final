from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http.request  import HttpRequest

from . import models

import subprocess
import sys



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
            return render(request, 'home/home.html')
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
