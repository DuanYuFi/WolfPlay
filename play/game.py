from play.models import Room, User
import json
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import uuid
from chats import getUsername, getUserId
from time import sleep

class Game:
    def __init__(self, room):
        self.channel_layer = get_channel_layer()
        self.room = room
        self.groupName = "chat_%s" % str(room.id)
        self.members = json.loads(room.members)
        self.wolfs = []
        self.hunter = ""
        self.witch = ""
        self.prophet = ""
        self.villagers = []
        self.count = len(self.members)
        self.wolfCount = 0
    
    def seperate(self):
        seperate = []
        random.shuffle(self.members)
        memberCount = self.count
        if memberCount == 2:
            seperate = [1, 1]
        if 6 <= memberCount <= 7:
            seperate = [2, memberCount - 3]
        elif memberCount <= 10:
            seperate = [3, memberCount - 5]
        else:
            seperate = [4, memberCount - 7]
        
        self.wolfs = self.members[:seperate[0]]
        self.wolfCount = seperate[0]
        self.villagers = self.members[seperate[0]:seperate[0] + seperate[1]]
        if memberCount - seperate[0] - seperate[1] != 0:
            self.witch = self.members[seperate[0] + seperate[1]]
        if memberCount - (seperate[0] + seperate[1]) - 1 != 0:
            self.prophet = self.members[seperate[0] + seperate[1] + 1]
        if memberCount - (seperate[0] + seperate[1]) - 2 != 0:
            self.hunter = self.members[-1]
    
    def sendMessage(self, message, Type):
        '''
        Type:
            "occupation-message": 职业信息
            "control": 发言控制
            "normal-content": 一般发言
            "statement": 游戏发言

        '''
        responseData = {}
        responseData['type'] = Type
        responseData['data'] = message
        async_to_sync(self.channel_layer.group_send)(self.groupName, {
            'type': 'sendMessage',
            'message': {'type': Type, 'data': message}
        })
    def systemMessage(self, message):
        submitData = {}
        submitData['user'] = "系统消息"
        submitData['content'] = message
        self.sendMessage(submitData, "normal-content")

    def start(self):
        self.seperate()
        self.occupation = {}
        for each in self.members:
            userName = getUsername(each)
            if each in self.villagers:
                self.occupation[userName] = '村民'
            elif each in self.wolfs:
                self.occupation[userName] = '狼人'
            elif each == self.hunter:
                self.occupation[userName] = '猎人'
            elif each == self.witch:
                self.occupation[userName] = '女巫'
            elif each == self.prophet:
                self.occupation[userName] = '预言家'
        self.sendMessage(self.occupation, 'occupation-message')
        random.shuffle(self.members)

        while self.wolfCount < self.count - self.wolfCount:
            self.systemMessage("狼人请选择淘汰对象")
            self.sendMessage("wolf", 'control')
            sleep(30)
            self.systemMessage("女巫阶段")
            self.sendMessage("witch", 'control')
            sleep(30)
            self.systemMessage("预言家阶段")
            self.sendMessage("prophet", "control")
            sleep(30)

            for each in self.members:
                self.systemMessage("请%s发言" % getUsername(each))
                self.sendMessage(getUsername(each), 'statement')
                sleep(60)

            self.systemMessage("请投票")
            self.sendMessage("", 'statement')
            
            self.count -= 1
        
        self.systemMessage("游戏结束")
