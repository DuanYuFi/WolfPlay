from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from play.models import User

# Create your views here.


def Register(request):
    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)

    check = User.objects.filter(name=post['username'])
    responseData = {}
    if check.count() != 0:
        responseData['msg'] = "False"
        responseData['code'] = 0
        responseData['check'] = False
        return HttpResponse(json.dumps(responseData))
    thisUser = User(name=post['username'],
                    password=post['password'], e_mail=post['email'])
    thisUser.save()

    responseData['code'] = 0
    responseData['msg'] = "OK"
    responseData['check'] = True
    return HttpResponse(json.dumps(responseData))


def Login(request):
    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)
    responseData = {}
    userInfo = {}
    userInfo['username'] = post['username']
    userInfo['IsAdmin'] = False
    try:
        checkUser = User.objects.filter(name=post['username'])
        checkUser = checkUser.get()
    except:
        responseData['userInfo'] = None
        responseData['code'] = -1
        responseData['token'] = ""
        responseData['expiresAt'] = ""
        responseData['msg'] = "用户名或密码错误"
        return HttpResponse(json.dumps(responseData))
    if checkUser.password != post['password']:
        responseData['code']=1
        responseData['userInfo']=None
        responseData['msg'] = "用户名或密码错误"
        return HttpResponse(json.dumps(responseData))
    else:
        userInfo['email']=checkUser.e_mail
        responseData['userInfo']=userInfo
        responseData['token']="asdasdasd"
        responseData['expiresAt']="2020/10/16"
        responseData['code']=0
        return HttpResponse(json.dumps(responseData))
