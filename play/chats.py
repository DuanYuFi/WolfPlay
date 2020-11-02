# pylint: disable=no-member

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from play.models import User, Room
import time
import uuid
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    responseData['code'] = 0
    responseData['msg'] = "ok"
    responseData['data'] = thisRoom.members

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
        responseData['msg'] = "The Room Already Exist!"
        responseData['data'] = ""
        return HttpResponse(json.dumps(responseData))

    newRoom = Room(name = post['name'], host = getUserId(post['username']))
    newRoom.save()

    addRoomMember(newRoom, newRoom.host)

    
    responseData['code'] = 0
    responseData['msg'] = "ok"
    responseData['data'] = str(newRoom.id)

    return HttpResponse(json.dumps(responseData))

def joinRoom(request):

    post = json.loads(request.body.decode('utf-8'))
    post = json.loads(post)

    print("user %s is in" % post['username'])

    responseData = {}
    if len(Room.objects.filter(name = post['name'])) == 0:
        responseData['code'] = 1
        responseData['msg'] = "Room not exist"
        responseData['data'] = ""
        return HttpResponse(json.dumps(responseData))
    
    thisUser = User.objects.filter(name = post['username'])[0]
    thisRoom = Room.objects.filter(name = post['name'])[0]
    addRoomMember(thisRoom, thisUser.id)
    thisUser.roomNumber = thisRoom.id

    thisUser.save()

    responseData['code'] = 0
    responseData['msg'] = "ok"
    responseData['data'] = str(thisRoom.id)

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

    if thisRoom.members == '[]':
        thisRoom.delete()
    responseData['code'] = 0
    responseData['msg'] = 'ok'
    return HttpResponse(json.dumps(responseData))

def startGame(roomName):

    thisRoom = Room.objects.filter(name = roomName)[0]
    members = json.loads(thisRoom.members)
    wolfs = []
    hunter = ""
    witch = ""
    prophet = ""
    villagers = []
    # seperate = [number of wolf, number of villagers]
    seperate = []
    random.shuffle(members)
    memberCount = len(members)
    if memberCount == 2:
        seperate = [1, 1]
    if 6 <= memberCount <= 7:
        seperate = [2, memberCount - 3]
    elif memberCount <= 10:
        seperate = [3, memberCount - 5]
    else:
        seperate = [4, memberCount - 7]
    
    wolfs = members[:seperate[0]]
    villagers = members[seperate[0]:seperate[0] + seperate[1]]
    if memberCount - seperate[0] - seperate[1] != 0:
        witch = members[seperate[0] + seperate[1]]
    if memberCount - (seperate[0] + seperate[1]) - 1 != 0:
        prophet = members[seperate[0] + seperate[1] + 1]
    if memberCount - (seperate[0] + seperate[1]) - 2 != 0:
        hunter = members[-1]
    
    channel_layer = get_channel_layer()
    groupName = "chat_%s" % str(thisRoom.id)

    occupation = {}
    for each in members:
        userName = getUsername(each)
        if each in villagers:
            occupation[userName] = '村民'
        elif each in wolfs:
            occupation[userName] = '狼人'
        elif each == hunter:
            occupation[userName] = '猎人'
        elif each == witch:
            occupation[userName] = '女巫'
        elif each == prophet:
            occupation[userName] = '预言家'
    
    data = {}
    data['type'] = 'occupation-message'
    data['data'] = occupation
    sendData = {}
    sendData['type'] = 'sendMessage'
    sendData['message'] = data

    async_to_sync(channel_layer.group_send)(groupName, sendData)


