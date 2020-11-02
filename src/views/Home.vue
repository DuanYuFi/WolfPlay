<template>
  <div>
    <div v-if="userInfo.username.length === 0">
      <div class="home">
        <h1>Welcome to WolfPlay</h1>
        <h1>Coming soon...</h1>
      </div>
    </div>
    <div v-else>
      <h1 style="padding-left: 10px">Welcome, {{ userInfo.username }} !</h1>
      <v-container class="fill-height warpper" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>加入/创建房间</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="loginForm" v-model="valid">
                  <v-text-field
                    v-model="roomName"
                    label="房间名"
                    name="room"
                    prepend-icon="mdi-account"
                    type="text"
                  />
                </v-form>
              </v-card-text>
              <v-alert v-if="invalid" dense outlined type="error">
                {{ errorMsg }}
              </v-alert>
              <v-card-actions>
                <v-spacer />
                <v-btn @click="createRoom" color="primary"> 创建 </v-btn>
                <v-btn @click="joinRoom" color="primary"> 进入 </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "home",
  data() {
    return {
      roomName: "",
      errorMsg: "",
      invalid: false,
    };
  },
  computed: {
    ...mapGetters("user", ["userInfo"]),
  },
  methods: {
    ...mapActions("user", ["newRoom", "joinRoomIn"]),
    createRoom() {
      console.log("In function createRoom");
      if (this.roomName.length !== 0) {
        var submitData = {};
        submitData.name = this.roomName;
        submitData.username = this.userInfo.username;
        const res = this.newRoom(submitData);
        console.log(res);
        res
          .then((code) => {
            console.log(code);
            this.$router.push({ name: "chat" });
          })
          .catch((error) => {
            this.errorMsg = error;
            this.invalid = true;
          });
      }
    },
    joinRoom() {
      if (this.roomName.length !== 0) {
        var submitData = {};
        submitData.name = this.roomName;
        submitData.username = this.userInfo.username;
        const res = this.joinRoomIn(submitData);
        console.log(res);
        res
          .then((code) => {
            console.log(code);
            this.$router.push({ name: "chat" });
          })
          .catch((error) => {
            this.errorMsg = error;
            this.invalid = true;
          });
      }
    },
  },
};
</script>

<style lang = "scss">
.home {
  text-align: center;
}
</style>