<template>
  <div>
    <div class="text-center">
      <v-snackbar v-model="snackbar" :timeout="timeout">
        {{ text }}
      </v-snackbar>
    </div>
    <div style="text-align: center;">
      {{userInfo.roomName}}
    </div>
    <v-container fluid style="padding: 0">
      <v-row>
        <v-col sm="2">
          <div class="namelist" style="text-align: center">
            <div
              class="username"
              v-for="(username, index) in members"
              v-bind:key="index"
            >
              [{{ index + 1 }}] {{ username }}
            </div>
          </div>
        </v-col>
        <v-col sm="10" style="position: relative">
          <div class="chat-container">
            <div
              class="message"
              v-for="(message, index) in chatMessages"
              v-bind:key="index"
              :class="{ own: message.user == username }"
            >
              <div
                class="username"
                v-if="index > 0 && messages[index - 1].user != message.user && message.user === username"
              >
                [{{occupation}}]{{ message.user }}
              </div>
              <div
                class = "username"
                v-else-if="index > 0 && messages[index - 1].user != message.user">
                {{ message.user }}
              </div>
              <div class="username" v-if="index == 0">
                {{ message.user }}
              </div>
              <div style="margin-top: 5px"></div>
              <div class="content" style="color: black">
                <div v-html="message.content"></div>
              </div>
            </div>
          </div>
          <div class="typer">
            <input
              :disabled="invalid"
              type="text"
              placeholder="Type here..."
              v-on:keyup.enter="sendMessage"
              v-model="content"
            />
            <v-spacer />
            <div v-if="userInfo.isHost">
              <v-btn @click="startGame"> Start Game </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// import Message from "@/components/message.vue";
import { mapGetters, mapActions } from "vuex";
import { getRoomMembers, gameStart } from "@/api/chat"

export default {
  data() {
    return {
      content: "",
      chatMessages: [],
      totalChatHeight: 0,
      websock: null,
      invalid: false,
      snackbar: false,
      timeout: 3000,
      occupation: "Visitor",
      text: "",
      blind: false,
      members: [],
      start: false,
    };
  },
  created() {
    console.log(this.userInfo);
    this.getUserList()
    this.initWebSocket();
  },
  destroyed() {
    let LeaveData = {};
    LeaveData.type = "Logout";
    LeaveData.data = this.username;
    this.websock.send(JSON.stringify(LeaveData));
    this.websock.close();
    this.removeHost();
    console.log(this.userInfo);
    this.leave();
  },
  computed: {
    ...mapGetters("user", ["userInfo"]),
    messages() {
      return this.chatMessages;
    },
    username() {
      return this.userInfo.username;
    },
  },
  watch: {
    // eslint-disable-next-line no-unused-vars
    "$route.params.id"(newId, oldId) {
      this.currentRef.off("child_added", this.onNewMessageAdded);
      this.loadChat();
    },
  },
  methods: {
    ...mapActions("user", ["leaveRoomOut", "removeHost"]),
    async getUserList() {
      let data = {}
      data['name'] = this.userInfo.roomName;
      const res = await getRoomMembers(data);
      console.log(res);
      this.members = res.data;
    },
    toHome() {
      this.$router.push({ name: "Home" });
    },
    async startGame() {
      this.start = true;
      let data = {};
      data['name'] = this.userInfo.roomID;
      const res = await gameStart(data);
      this.members = res.data;
      this.invalid = true;
    },
    leave() {
      let submitData = {};
      submitData["name"] = this.userInfo.roomID;
      submitData["username"] = this.userInfo.username;
      this.leaveRoomOut(submitData);
      this.$router.push({ name: "Home" });
    },
    sendMessage() {
      if (this.content != "") {
        console.log(this.content);
        this.websocketsend(this.content);
        this.content = "";
      }
    },
    initWebSocket() {
      console.log("Initing...");
      //初始化weosocket
      const wsuri =
        "ws://10.21.142.235:8001/ws/chat/" + this.userInfo.roomID + "/";
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onopen = this.websocketonopen;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
      console.log("Websocket inited!");
      console.log(this.websock);
    },
    websocketonopen() {
      //连接建立之后执行send方法发送数据
      let actions = {};
      actions.type = "newLogin";
      actions.data = this.username;
      this.websock.send(JSON.stringify(actions));
      // this.websocketsend(JSON.stringify(actions));
      // console.log("Send succeed!");
    },
    websocketonerror() {
      //连接建立失败重连
      console.log("Connection error");
      this.initWebSocket();
    },
    websocketonmessage(e) {
      //数据接收
      const redata = JSON.parse(e.data);
      console.log(redata)
      if (redata["type"] === "normal-content") {
        if (!this.blind) {
          this.chatMessages.push(redata);
          console.log(redata);
          if (redata.name === self.username) {
            this.scrollToEnd();
          }
        }
      } else if (redata["type"] === "occupation-message") {
        console.log("received occupation-message");
        let occupations = redata["data"];
        console.log(this.userInfo.username)
        this.occupation = occupations[this.userInfo.username];
        this.text = "你的职业是：" + this.occupation;
        this.messages.push({"user": "Occupation", "content": this.text});
        this.start = true;
      } else if (redata["type"] === "control") {
        if (redata["data"] === "daytime") {
          this.invalid = true;
          this.blind = false;
        } else if (this.occupation !== redata["data"]) {
          this.invalid = true;
          this.blind = true;
        } else {
          this.invalid = false;
          this.blind = false;
        }
      } else if (redata["type"] === "statement") {
        if (this.username === redata["data"]) {
          this.invalid = false;
          this.blind = false;
        } else {
          this.invalid = true;
          this.blind = false;
        }
      } else if (redata["type"] === "newLogin") {
        if (this.members.indexOf(redata["data"]) === -1) {
          this.members.push(redata["data"]);
        }
      } else if (redata['type'] === 'Logout') {
        let index = this.members.indexOf(redata['data']);
        if (index !== -1) {
          this.members.splice(index, 1);
        }
      } else if (redata['type'] === 'free') {
        this.invalid = false;
        this.blind = false;
      } else if (redata['type'] === 'Gameover') {
        this.occupation = 'Visitor';
      }
    },
    websocketsend(Data) {
      //数据发送
      var processedData = this.processMessage(Data);
      var responseData = {};
      if (Data[0] == "/" && Data[1] != '/' && this.start) {
        var data2 = {};
        data2.occupation = this.occupation;
        data2.data = Data;
        data2.name = this.username;
        responseData.type = "game-control";
        responseData.data = data2;
      } else {
        responseData.type = "normal-content";
        responseData.content = processedData;
        responseData.user = this.username;
      }
      this.websock.send(JSON.stringify(responseData));
      // console.log("Data sent");
    },
    websocketclose() {
      //关闭
      console.log("断开连接");
    },
    test() {
      this.$nextTick(() => {
        var container = this.$el.querySelector(".chat-container");
        console.log(container.scrollTop);
        console.log(container.scrollHeight);
      });
    },
    processMessage(message) {
      /*eslint-disable */
      var urlPattern = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gi;
      /*eslint-enable */
      message = message
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
      message = message.replace(urlPattern, "<a href='$1'>$1</a>");
      return message;
    },
    scrollToEnd() {
      this.$nextTick(() => {
        var container = this.$el.querySelector(".chat-container");
        container.scrollTop = container.scrollHeight;
      });
    },
  },
};
</script>

<style>
.scrollable {
  overflow-y: auto;
  height: 90vh;
}
.typer {
  box-sizing: border-box;
  display: flex;
  align-items: center;
  bottom: 0;
  height: 4.9rem;
  width: 100%;
  background-color: #292929;
  box-shadow: 0 -5px 10px -5px rgba(0, 0, 0, 0.2);
}
.typer input[type="text"] {
  position: absolute;
  left: 2.5rem;
  padding: 1rem;
  width: 80%;
  background-color: transparent;
  border: none;
  outline: none;
  font-size: 1.25rem;
  color: white;
}
.chat-container {
  box-sizing: border-box;
  height: calc(100vh - 10rem);
  overflow-y: auto;
  background-color: #222222;
  padding: 10px;
}
.message {
  margin-bottom: 3px;
}
.message.own {
  text-align: right;
}
.message.own .content {
  background-color: lightskyblue;
}
.chat-container .username {
  font-size: 18px;
  font-weight: bold;
}
.chat-container .content {
  padding: 8px;
  background-color: lightgreen;
  border-radius: 10px;
  display: inline-block;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14),
    0 2px 1px -1px rgba(0, 0, 0, 0.12);
  max-width: 50%;
  word-wrap: break-word;
}
@media (max-width: 480px) {
  .chat-container .content {
    max-width: 60%;
  }
}
</style>
