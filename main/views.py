# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login
from .models import User, Algorithm
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import SignupForm, AlgorithmForm


def index(request):
    if request.session.get('user_id') is not None:
        return HttpResponseRedirect('/editor/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                print('Attempt to check user')
                User.objects.get(username=username)
                user = authenticate(request, username=username, password=password)
                if user is None:
                    return HttpResponse("<h1>Failed to authenticate!</h1>")
                else:
                    request.session["user_id"] = user.id
                    return HttpResponseRedirect('/editor/')
            except User.DoesNotExist:
                print('Attempt to add new user')
                user = User.objects.create_user(username=username, password=password)
                user.save()
                user = authenticate(request, username=username, password=password)
                if user is None:
                    return HttpResponse("<h1>Failed to authenticate!</h1>")
                else:
                    request.session["user_id"] = user.id
                    return HttpResponseRedirect('/editor/')


    else:
        form = SignupForm()
    return render(request, 'main/index.html', {'form': form})


def algorithm(request, current):
    form = AlgorithmForm()
    out = ""
    if request.method == 'POST':
        form = AlgorithmForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            owner = request.session.get("user_id")
            algo = Algorithm.objects.get(id=current)
            algo.delete()
            algo = Algorithm.objects.create(id=current, name=name, owner=owner, code=code)
            algo.save()
            out = execute(code, name)

    try:
        current = Algorithm.objects.get(id=current)
        form = AlgorithmForm(data={"name": current.name, "code": current.code})
        out = execute(current.code, current.name)
        context = {
            "user": request.session.get("user_id"),
            "algorithms": Algorithm.objects.filter(owner=request.session.get("user_id")),
            "current": current,
            "form": form,
            "out": out
        }
    except Algorithm.DoesNotExist:
        context = {"form": form, "user": request.session.get("user_id"), "out": out}
    return render(request, 'main/editor.html', context)


def editor(request):
    if request.method == 'POST':
        form = AlgorithmForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            owner = request.session.get("user_id")
            algo = Algorithm.objects.create(name=name, code=code, owner=owner)
            algo.save()
            return HttpResponseRedirect('/algorithm/' + str(algo.id))
    try:
        owner = request.session.get("user_id")
        context = {
            "user": request.session.get("user_id"),
            "form": AlgorithmForm(),
            "algorithms": Algorithm.objects.filter(owner=owner),
        }

    except Algorithm.DoesNotExist:
        context = {"form": AlgorithmForm(),
                   "user": request.session.get("user_id")
                   }
    return render(request, 'main/editor.html', context)


import os
import subprocess

executing_path = os.path.abspath(__file__)
executing_path = executing_path[0:len(executing_path) - 9]


def process(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.communicate()


def compl(filenameCompile, code):
    try:
        f = open(filenameCompile, 'a', encoding='utf-8')
        f.write(code)
        f.close()
        cmd = 'javac ' + filenameCompile
        outCompile = process(cmd)
        return outCompile
    except Exception as e:
        return str(e)


def exect(filenameExec):
    try:
        cmd = 'java ' + filenameExec
        outExec = process(cmd)
        return outExec
    except Exception as e:
        return str(e)


def clear(filename):
    try:
        os.remove(filename)
    except Exception as e:
        print(e)


def execute(code, name):
    filenameCompile = executing_path + '/' + name + '.java'
    filenameExec = executing_path + '/' + name

    c = compl(filenameCompile, code)
    e = exect(filenameExec)

    clear(filenameExec)
    clear(filenameCompile)

    output = c + e
    result = []
    for item in output:
        result.append(str(item))
    return "\n".join(result)


def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/')