<template>
  <div>
    <v-toolbar dark prominent height="58px">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <div class="title-without-decoration">
        <router-link to="/">
          <v-toolbar-title
            style="margin-top: 7px; color: white; margin-left: 5px"
            >Wolf Play</v-toolbar-title
          >
        </router-link>
      </div>
      <v-spacer></v-spacer>

      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn dark icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list min-height="40px" min-width="400px">
          <v-list-item v-for="(item, i) in items" :key="i" link>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-toolbar>

    <v-navigation-drawer v-model="drawer" absolute bottom temporary app>
      <v-list nav dense>
        <v-list-item-group v-model="group">
          <v-list-item>
            <v-list-item-title>游戏</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>好友</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>个人资料</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>帮助</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <template v-slot:append>
        <div v-if="userInfo.username.length === 0" >
            <div class="pa-2">
            <v-btn block to="/register"> 注册 </v-btn>
            </div>
            <div class="pa-2">
            <v-btn block to="/login"> 登录 </v-btn>
            </div>
        </div>
        <div v-else>
            <div class="pa-2">
            <v-btn block> 个人信息 </v-btn>
            </div>
            <div class="pa-2">
            <v-btn block
                @click = "LoginOut"
            > 登出 </v-btn>
            </div>
        </div>
      </template>
    </v-navigation-drawer>

    <v-card-text> </v-card-text>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Bar",
  data: () => ({
    drawer: false,
    group: null,
    search: false,
    isLoggedIn: false,
    items: [{ title: "关于" }, { title: "帮助" }, { title: "捐款" }],
  }),
  computed: {
    ...mapGetters("user", ["userInfo", "token"]),
  },
  watch: {
    group() {
      this.drawer = false;
    },
  },
  methods: {
    ...mapActions("user", ["LoginOut"]),
    isHome(route) {
      return route.name === "home";
    },
  },
};
</script>

<style lang = "scss">
.drawer_header {
  text-decoration: none;
  margin: 0;
  height: 56px;
  h1 {
    text-align: center;
  }
}
.title-without-decoration {
  a {
    text-decoration: none;
    text-align: center;
  }
}
</style>