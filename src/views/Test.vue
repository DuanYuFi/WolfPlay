<!--<template>
  <div class="title">
    <h1>{{ userInfo }}</h1>
    <v-text-field
      v-model = "Form.name"
    />
    <v-btn @click = "submit">Submit</v-btn>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import service from '@/utils/request'
export default {
  name: "Test",
  data() {
    return {
      Form : {
        name: ""
      }
    }
  },
  computed: {
    ...mapGetters("user", ["userInfo", "token"]),
  },
  methods: {
    async submit() {
      const res = await service({
        url: '/user/test/',
        method: 'post',
        data: JSON.stringify(this.Form)
      });
      console.log(res.data)
    }
  }
}
</script>

<style lang = "scss">
.title {
  text-align: center;
}
</style>-->
<template>
  <div class="test">
    <p>{{ messages }}</p>
    <v-btn @click = "test">Submit</v-btn>
  </div>
</template>

<script>
  export default {
    name : 'test',
    data() {
      return {
        messages: "",
        websock: null,
      }
    },
    created() {
      this.initWebSocket();
    },
    destroyed() {
      this.websock.close() //离开路由之后断开websocket连接
    },
    methods: {
      initWebSocket(){ //初始化weosocket
        const wsuri = "ws://10.21.142.235:8001/ws/chat/";
        this.websock = new WebSocket(wsuri);
        this.websock.onmessage = this.websocketonmessage;
        this.websock.onopen = this.websocketonopen;
        this.websock.onerror = this.websocketonerror;
        this.websock.onclose = this.websocketclose;
        console.log("Websocket inited!");
        console.log(this.websock)
      },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        console.log("WebSocket opened!");
      },
      websocketonerror(){//连接建立失败重连
        console.log("Connection error");
        this.initWebSocket();
      },
      websocketonmessage(e){ //数据接收
        const redata = JSON.parse(e.data);
        this.messages += redata;
        console.log(redata);
      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
        console.log("Data sent");
      },
      websocketclose(){  //关闭
        console.log('断开连接');
      },
      test() {
        var responseData = {};
        responseData.content = "another message";
        responseData.user = "DuanYuFi";
        responseData.room = "12123";
        this.websocketsend(JSON.stringify(responseData));
        console.log(this.websock);
      }
    },
  }
</script>
<style lang='less'>
 
</style>
