# pylint: disable=no-member

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from play.models import User, Room, Game
import time
from time import sleep
import uuid
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from play.game import PlayGame
from multiprocessing import Process

Games = {}

def getRoomByUser(userName):
    '''
        give a userName and return a Room object that the person in
    '''
    thisUser = User.objects.filter(name = userName)[0]
    roomID = thisUser.roomNumber
    return Room.objects.filter(id = roomID)[0]

def sendMessage(request):
    '''
        requery:
            struct of data
            data {
                name: string, 
                content: string,
                time: string
            }
        return:
            responseData {
                code: int, 
            }
    '''
    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)
    thisRoom = getRoomByUser(post['name'])
    thisContent = {}
    thisContent['content'] = post['content']
    thisContent['user'] = post['name']
    localtime = post['time']
    thisContent['time'] = localtime
    thisRoomChat = json.loads(thisRoom.chats)
    thisRoomChat.append(thisContent)
    thisRoom.chats = json.dumps(thisRoomChat)
    thisRoom.save()
    responseData = {}
    responseData['code'] = 0
    return HttpResponse(json.dumps(responseData))

def getRoomMembers(request):
    '''
        requery:
            struct of data:
            data {
                name: string
            }
        
        return responseData {
            code: int, 
            msg: string,
            data: string of list
        }
    '''
    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)
    roomName = post['name']
    responseData = {}
    if len(Room.objects.filter(name = roomName)) == 0:
        responseData['code'] = 1
        responseData['msg'] = "Room Not Exist"
        responseData['data'] = None
        return HttpResponse(json.dumps(responseData))
    
    thisRoom = Room.objects.filter(name = roomName)[0]
    RoomMembers = json.loads(thisRoom.members)
    member = []

    for each in RoomMembers:
        member.append(getUsername(each))

    responseData['code'] = 0
    responseData['msg'] = "ok"
    responseData['data'] = member

    return HttpResponse(json.dumps(responseData))

def getRoomChats(request):
    '''
        requery:
            struct of data:
            data {
                name: string
            }
        
        return responseData {
            code: int, 
            msg: string,
            data: json string of list
        }
    '''
    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)
    thisRoom = getRoomByUser(post['name'])
    responseData = {}
    responseData['code'] = 0
    responseData['msg'] = 'ok'
    responseData['data'] = json.loads(thisRoom.chats)
    return HttpResponse(json.dumps(responseData))

def addRoomMember(room, member):
    members = json.loads(room.members)
    if str(member) not in members:
        members.append(str(member))
        room.members = json.dumps(members)
        room.save()

def deleteRoomMember(room, member):
    members = json.loads(room.members)
    if str(member) in members:
        members.remove(str(member))
        room.members = json.dumps(members)
        room.save()

def getUserId(username):
    try:
        user = User.objects.filter(name = username)[0]
    except:
        return None
    
    return user.id

def getUsername(userID):
    try:
        user = User.objects.filter(id = uuid.UUID(userID))[0]
    except:
        return None
    
    return user.name

def createRoom(request):

    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)
    responseData = {}

    if len(Room.objects.filter(name = post['name'])) != 0:
        responseData['code'] = 1
        responseData['msg'] = "房间已存在"
        responseData['data'] = ""
        return HttpResponse(json.dumps(responseData))

    newRoom = Room(name = post['name'], host = getUserId(post['username']), password = post['password'])
    newRoom.save()

    addRoomMember(newRoom, newRoom.host)
    newGame = Game(name = post['name'])
    newGame.save()

    responseData['code'] = 0
    responseData['msg'] = "ok"
    responseData['data'] = (str(newRoom.id), newRoom.name)

    return HttpResponse(json.dumps(responseData))

def joinRoom(request):

    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)

    print("user %s is in" % post['username'])

    responseData = {}
    if len(Room.objects.filter(name = post['name'])) == 0:
        responseData['code'] = 1
        responseData['msg'] = "房间不存在"
        responseData['data'] = ""
        return HttpResponse(json.dumps(responseData))
    
    thisUser = User.objects.filter(name = post['username'])[0]
    thisRoom = Room.objects.filter(name = post['name'])[0]

    if thisRoom.password != post['password']:
        responseData['code'] = 1
        responseData['msg'] = "密码错误"
        responseData['data'] = ""
        return HttpResponse(json.dumps(responseData))

    addRoomMember(thisRoom, thisUser.id)
    thisUser.roomNumber = thisRoom.id

    thisUser.save()

    responseData['code'] = 0
    responseData['msg'] = "ok"
    responseData['data'] = [str(thisRoom.id), thisRoom.name]

    return HttpResponse(json.dumps(responseData))

def leaveRoom(request):
    
    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)
    
    print("user %s is leave from %s" % (post['username'], post['name']))
    thisRoom = Room.objects.filter(id = post['name'])[0]
    responseData = {}
    thisUser = User.objects.filter(name = post['username'])[0]
    deleteRoomMember(thisRoom, thisUser.id)
    thisUser.roomNumber = uuid.UUID("00000000-0000-0000-0000-000000000000")
    thisUser.save()
    if Games[post['name']].is_alive():
        Games[post['name']].terminate()
        Games.pop(post['name'])
    if thisRoom.members == '[]':
        thisRoom.delete()
    responseData['code'] = 0
    responseData['msg'] = 'ok'
    return HttpResponse(json.dumps(responseData))

def startGame(request):
    global Games
    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)

    thisRoom = Room.objects.filter(id = post['name'])[0]
    Games[post['name']] = PlayGame(thisRoom)

    members = []
    tmp = Games[post['name']].members
    for each in tmp:
        members.append(getUsername(each))
    responseData = {}
    responseData['code'] = 0
    responseData['msg'] = "ok"
    responseData['data'] = members
    Games[post['name']].start()
    # p = Process(target=test)
    # p.start()
    # print(responseData)
    return HttpResponse(json.dumps(responseData))

def test():
    print("In Test")
    group_name = "chat_49ae80b8-6717-4e6c-8ab2-2c0262315edd"
    channel_layer = get_channel_layer()
    data = {}
    data['type'] = 'normal-content'
    data['user'] = 'function'
    data['content'] = 'Test'

    async_to_sync(channel_layer.group_send)(group_name, {
        'type': 'sendMessage',
        'message': data
    })
