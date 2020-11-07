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
    try:
        if Data['type'] == 'vote' and Data['data'][:5] == '/vote':
            now = json.loads(thisGame.vote)
            now[Data['name']] = int(Data['data'][6:])
            thisGame.vote = json.dumps(now)
            thisGame.save()
        elif Data['occupation'] == '狼人' and Data['data'][:7] == '/choose':
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
    except:
        pass


class PlayGame(Thread):
    def __init__(self, room):
        Thread.__init__(self)
        self.isPlaying = False
        self.channel_layer = get_channel_layer()
        self.room = room
        self.roomName = room.name
        self.groupName = "chat_%s" % str(room.id)
        self.members = json.loads(room.members)     # id
        self.wolfs = []     # id
        self.hunter = ""
        self.witch = ""
        self.prophet = ""
        self.villagers = []  # id
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
        elif memberCount == 4:
            seperate = [1, 1]
        elif memberCount == 5:
            seperate = [2, 1]
        elif 6 <= memberCount <= 7:
            seperate = [2, memberCount - 3]
        elif memberCount <= 10:
            seperate = [3, memberCount - 5]
        else:
            seperate = [4, memberCount - 7]

        self.wolfs = self.members[:seperate[0]]
        self.wolfCount = seperate[0]
        self.villagers = self.members[seperate[0]:seperate[0] + seperate[1]]
        if memberCount == 4:
            self.witch = self.members[2]
            self.prophet = self.members[3]
        if memberCount == 5:
            self.witch = self.members[3]
            self.prophet = self.members[4]
        else:
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

    def systemMessage(self, message, to):
        submitData = {}
        submitData['user'] = "系统消息"
        submitData['content'] = message
        submitData['to'] = to
        self.sendMessage(submitData, "System")

    def vote(self, data):
        choices = {}
        maxCount = 0
        member = None
        for each in data:
            if self.alive[str(getUserId(each))]:
                choices[data[each]] = 0
        for each in data:
            if self.alive[str(getUserId(each))]:
                choices[data[each]] += 1

        for each in data:
            if choices[data[each]] > maxCount and self.alive[str(getUserId(each))]:
                (maxCount, member) = (choices[data[each]], data[each])
        return member

    def alives(self, to):
        msg = "当前存活:<br />"
        for each in self.alive:
            if self.alive[each]:
                msg += "%s<br />" % getUsername(each)

        self.systemMessage(msg, to)

    def run(self):     # real run
        names = []
        for each in self.members:
            self.alive[each] = True
            names.append(getUsername(each))
        self.sendMessage({'data': names}, 'members')
        self.isPlaying = True
        self.sendMessage({'data': self.occupation}, 'occupation-message')
        while self.wolfCount < self.count - self.wolfCount and self.wolfCount != 0:
            killed = []     # names

            self.systemMessage("狼人阶段", "All")
            self.sendMessage({'data': "狼人"}, 'control')
            self.systemMessage('狼人请选择淘汰对象, 以"/choose 序号"的形式发送', "狼人")
            self.alives("狼人")

            start = time()
            while time() - start < 60:
                self.db.refresh_from_db()
                if len(json.loads(self.db.wolf_choices)) == self.wolfCount:
                    break
                sleep(1)
            self.db.refresh_from_db()

            self.systemMessage("女巫阶段", "All")
            self.sendMessage({'data': "女巫"}, 'control')
            self.systemMessage('以"/kill 序号"或者"/save 序号"的形式发送', "女巫")
            self.alives("女巫")
            self.systemMessage("你还有%d瓶毒药，%d瓶解药" %
                               (self.db.witchPoison, self.db.witchAntidote), "女巫")
            if len(json.loads(self.db.wolf_choices)) != 0:
                killed.append(getUsername(
                    self.members[self.vote(json.loads(self.db.wolf_choices)) - 1]))
                self.systemMessage("%s 将要被杀" % killed[0], "女巫")
            else:
                self.systemMessage("无人被杀", "女巫")

            self.db.wolf_choices = "{}"
            self.db.save()

            start = time()
            while time() - start < 60:
                self.db.refresh_from_db()
                if self.db.witch_choice != '':
                    break
                sleep(1)

            self.db.refresh_from_db()
            if self.db.witch_choice != "":
                choice = self.members[int(self.db.witch_choice) - 1]
                if getUsername(choice) == killed[0] and self.db.witchAntidote == 1:
                    self.db.witchAntidote = 0
                    killed = []
                elif self.db.witchPoison == 1:
                    self.db.witchPoison = 0
                    killed.append(getUsername(choice))

            self.db.witch_choice = ""
            self.db.save()
            self.systemMessage("预言家阶段", 'All')
            self.sendMessage({'data': "预言家"}, "control")
            self.systemMessage('以"/check 序号"的形式发送', "预言家")
            self.alives("预言家")

            start = time()
            while time() - start < 60:
                self.db.refresh_from_db()
                if self.db.prophet_choice != '':
                    break
                sleep(1)

            if len(self.db.prophet_choice) != 0:
                if self.members[int(self.db.prophet_choice) - 1] in self.wolfs:
                    self.systemMessage("%s:坏人" % getUsername(
                        self.members[int(self.db.prophet_choice) - 1]), "预言家")
                else:
                    self.systemMessage("%s:好人" % getUsername(
                        self.members[int(self.db.prophet_choice) - 1]), "预言家")

            self.db.prophet_choice = ""
            self.db.save()

            self.sendMessage({'data': "daytime"}, "control")
            if len(killed) == 0:
                self.systemMessage("天亮了 昨晚无人死亡", "All")
            else:
                msg = "天亮了 昨晚"
                for each in killed:
                    msg = msg + each + " "
                msg += "死亡"
                self.systemMessage(msg, "All")

            for each in killed:
                if self.alive[str(getUserId(each))]:
                    self.count -= 1
                    self.alive[str(getUserId(each))] = False
                    if str(getUserId(each)) in self.wolfs:
                        self.wolfCount -= 1
            killed = []
            sleep(3)
            if self.wolfCount == 0 or self.wolfCount >= self.count - self.wolfCount:
                if self.wolfCount == 0:
                    self.systemMessage("好人胜利", "All")
                else:
                    self.systemMessage("狼人胜利", "All")
                break
            self.systemMessage("发言阶段，每人15s", "All")
            for each in self.members:
                if self.alive[each]:
                    self.systemMessage("请%s发言" % getUsername(each), "All")
                    self.sendMessage({'data': getUsername(each)}, 'statement')
                    sleep(15)

            self.systemMessage('30s请投票, 输入"/vote id"', "All")
            self.sendMessage({}, 'vote')
            start = time()
            while time() - start < 15:
                self.db.refresh_from_db()
                if len(json.loads(self.db.vote)) == self.count:
                    break
                sleep(1)

            if self.db.vote != '{}':
                self.systemMessage("%s 死了" % getUsername(
                    self.members[self.vote(json.loads(self.db.vote)) - 1]), "All")
                killed.append(getUsername(
                    self.members[self.vote(json.loads(self.db.vote)) - 1]))
                self.db.vote = '{}'
                self.db.save()
            else:
                self.systemMessage("无人投票", "All")
            for each in killed:
                if self.alive[str(getUserId(each))]:
                    self.count -= 1
                    self.alive[each] = False
                    if str(getUserId(each)) in self.wolfs:
                        self.wolfCount -= 1
            self.alives("All")

        self.systemMessage("游戏结束", "All")
        self.isPlaying = False
        self.db.delete()

    def run2(self):  # test
        # sleep(3)
        names = []
        for each in self.members:
            names.append(getUsername(each))
        self.sendMessage({'data': names}, 'members')
        self.sendMessage({'data': self.occupation}, 'occupation-message')

        #self.systemMessage('狼人请选择淘汰对象, 以"/choose 序号"的形式发送')
        #self.alives()
        self.sendMessage({'data': "狼人"}, 'control')

        start = time()
        while time() - start < 10:
            self.db.refresh_from_db()
            if len(json.loads(self.db.wolf_choices)) == len(self.wolfs):
                break
            sleep(1)
            print(time())
        self.db.refresh_from_db()
        self.sendMessage({}, "free")
        # if self.db.wolf_choices != '{}':
        #     #self.systemMessage("%s 死了" % getUsername(
        #     #    self.members[self.vote(json.loads(self.db.wolf_choices)) - 1]))
        # else:
        #     #self.systemMessage("No input")
        # #self.systemMessage("Game over")
        # self.sendMessage({}, 'Gameover')
