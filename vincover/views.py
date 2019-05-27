from django.shortcuts import render
from django.http.response import HttpResponse


from vincover.models import User
import json


def regist(request):
    return render(request,'vincover/regist.html')

def registlogic(request):
    name=request.POST.get('username')
    userpwd = request.POST.get('userpwd')
    confirmpwd= request.POST.get('confirmpwd')
    print(name,userpwd,confirmpwd)
    if userpwd == confirmpwd:
        return HttpResponse('注册成功')
    return HttpResponse('注册失败')

def checkname(request):
    name=request.GET.get('username')
    user=User.objects.filter(name=name)
    name2=User.objects.get(pk='1').name
    print('name=',name)
    print(name2)
    print(user)
    if user:
        return HttpResponse('账号已经注册')
    return HttpResponse('账号可以注册')


def checkpwd(request):
    userpwd=request.GET.get('userpwd')
    confirmpwd=request.GET.get('confirmpwd')
    if len(userpwd) < 6:
        return HttpResponse('密码长度不能少于6位数')
    else:
        return HttpResponse('密码符合规范要求')


def checkconfirmpwd(request):
    userpwd=request.GET.get('userpwd')
    confirmpwd=request.GET.get('confirmpwd')
    if userpwd == confirmpwd:
        return HttpResponse('两次密码输入一致')
    else:
        return HttpResponse('两次密码输入不一致')