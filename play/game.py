# pylint: disable=no-member
from play.models import Room, User, Game
import json
import random
from asgiref.sync import async_to_sync
import uuid
from time import sleep, time
from threading import Thread

from channels.layers import get_channel_layer
from multiprocessing import Process


def getUserId(username):
    try:
        user = User.objects.filter(name=username)[0]
    except:
        return None

    return user.id


def getUsername(userID):
    try:
        user = User.objects.filter(id=uuid.UUID(userID))[0]
    except:
        return None

    return user.name


def processData(Data, roomID):
    thisGame = Game.objects.filter(name=roomID)[0]
    print(Data)
    if Data['occupation'] == '狼人' and Data['data'][:7] == '/choose':
        now = json.loads(thisGame.wolf_choices)
        now[Data['name']] = int(Data['data'][8:])
        thisGame.wolf_choices = json.dumps(now)
        thisGame.save()
    elif Data['occupation'] == '女巫' and (Data['data'][:5] == '/save' or Data['data'][:5] == '/kill'):
        thisGame.witch_choice = Data['data'][6:]
        thisGame.save()
    elif Data['occupation'] == '预言家' and Data['data'][:6] == '/check':
        thisGame.prophet_choice = Data['data'][7:]
        thisGame.save()


class PlayGame(Thread):
    def __init__(self, room):
        Thread.__init__(self)
        self.isPlaying = False
        self.channel_layer = get_channel_layer()
        self.room = room
        self.roomName = room.name
        self.groupName = "chat_%s" % str(room.id)
        self.members = json.loads(room.members)     # id
        self.wolfs = []
        self.hunter = ""
        self.witch = ""
        self.prophet = ""
        self.villagers = []
        self.count = len(self.members)
        self.wolfCount = 0
        self.alive = {}     # index = id
        self.db = Game(name=room.id)
        self.seperate()
        self.occupation = {}
        self.db.save()
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

        random.shuffle(self.members)

    def seperate(self):
        seperate = []
        random.shuffle(self.members)
        memberCount = self.count
        if memberCount == 2:
            seperate = [1, 1]
        elif 6 <= memberCount <= 7:
            seperate = [2, memberCount - 3]
        elif memberCount <= 10:
            seperate = [3, memberCount - 5]
        else:
            seperate = [4, memberCount - 7]

        self.wolfs = self.members[:seperate[0]]
        self.wolfCount = seperate[0]
        self.villagers = self.members[seperate[0]:seperate[0] + seperate[1]]
        if memberCount - seperate[0] - seperate[1] > 0:
            self.witch = self.members[seperate[0] + seperate[1]]
        if memberCount - (seperate[0] + seperate[1]) - 1 > 0:
            self.prophet = self.members[seperate[0] + seperate[1] + 1]
        if memberCount - (seperate[0] + seperate[1]) - 2 > 0:
            self.hunter = self.members[-1]
        for each in self.members:
            self.alive[each] = True

    def sendMessage(self, message, Type):
        '''
        Type:
            "occupation-message": 职业信息
            "control": 发言控制
            "normal-content": 一般发言
            "statement": 游戏发言

        '''

        message['type'] = Type
        # print(self.channel_layer)
        # print("send " + str(message))

        async_to_sync(self.channel_layer.group_send)(self.groupName, {
            'type': 'sendMessage',
            'message': message
        })

    def systemMessage(self, message):
        submitData = {}
        submitData['user'] = "系统消息"
        submitData['content'] = message
        self.sendMessage(submitData, "normal-content")

    def vote(self, data):
        choices = {}
        maxCount = 0
        member = None
        for each in data:
            choices[data[each]] = 0
        for each in data:
            choices[data[each]] += 1
        for each in data:
            if choices[data[each]] > maxCount:
                (maxCount, member) = (choices[data[each]], data[each])
        return member

    def run2(self):     # real run
        self.isPlaying = True
        self.sendMessage({'data': self.occupation}, 'occupation-message')
        while self.wolfCount < self.count - self.wolfCount:
            killed = []     # names
            self.systemMessage('狼人请选择淘汰对象, 以"/choose 序号"的形式发送')
            self.sendMessage("wolf", 'control')

            start = time()
            while time() - start < 30:
                self.db.refresh_from_db()
                if len(json.loads(self.db.wolf_choice)) == len(self.wolfs):
                    break
                sleep(1)
            self.db.refresh_from_db()

            self.sendMessage("witch", 'control')
            self.systemMessage('女巫阶段, 以"/kill 序号"或者"/save 序号"的形式发送')
            if len(json.loads(self.db.wolf_choice)) != 0:
                killed.append(self.members[self.vote(
                    json.loads(self.wolf_choice))])
                self.systemMessage("%s 将要被杀" % killed[0])
            else:
                self.systemMessage("无人被杀")

            self.db.wolf_choices = "{}"
            self.db.save()

            start = time()
            while time() - start < 30:
                self.db.refresh_from_db()
                if self.db.witch_choice != '':
                    break
                sleep(1)

            if self.db.witch_choice == killed[0]:
                killed = []
            else:
                killed.append(self.db.witch_choice)

            self.db.witch_choice = ""
            self.db.save()

            self.systemMessage('预言家阶段, 以"/check 序号"的形式发送')
            self.sendMessage("prophet", "control")

            start = time()
            while time() - start < 30:
                self.db.refresh_from_db()
                if self.db.prophet_choice != '':
                    break
                sleep(1)

            if len(self.db.prophet_choice) != 0:
                if getUserId(self.db.prophet_choice) in self.wolfs:
                    self.systemMessage("好人")
                else:
                    self.systemMessage("坏人")

            self.db.prophet_choice = ""
            self.db.save()

            self.sendMessage("daytime", "control")
            if len(killed) == 0:
                self.systemMessage("天亮了 昨晚无人死亡")
            else:
                msg = "天亮了 昨晚"
                for each in killed:
                    msg = msg + each + ""
                    if getUserId(each) in self.wolfs:
                        wolfCount -= 1
                    self.count -= 1
                msg += "死亡"
                self.systemMessage(msg)

            for each in self.members:
                self.systemMessage("请%s发言" % getUsername(each))
                self.sendMessage(getUsername(each), 'statement')
                sleep(60)

            self.systemMessage("请投票")
            self.sendMessage("", 'statement')

            self.count -= 1

        self.systemMessage("游戏结束")
        self.isPlaying = False
    def run(self):  # test
        # sleep(3)
        self.sendMessage({'data': ""}, 'statement')
        self.systemMessage("Test")
        self.sendMessage({'data': self.occupation}, 'occupation-message')
        
        self.systemMessage('狼人请选择淘汰对象, 以"/choose 序号"的形式发送')
        self.sendMessage({'data':"狼人"}, 'control')

        start = time()
        while time() - start < 10:
            self.db.refresh_from_db()
            if len(json.loads(self.db.wolf_choices)) == len(self.wolfs):
                break
            sleep(1)
            print(time())
        self.db.refresh_from_db()
        self.sendMessage({}, "free")
        if self.db.wolf_choices != '{}':
            self.systemMessage("%s 死了" % getUsername(self.members[self.vote(json.loads(self.db.wolf_choices)) - 1]))
        else:
            self.systemMessage("No input")
        self.systemMessage("Game over")
        self.sendMessage({}, 'Gameover')
