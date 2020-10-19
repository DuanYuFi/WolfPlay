<template>
  <div class="login">
    <vue-particles
      color="#dedede"
      :particle-opacity="0.8"
      :particles-number="50"
      shape-type="circle"
      :particle-size="12"
      lines-color="#dedede"
      :lines-width="1"
      :line-linked="true"
      :line-opacity="0.4"
      :lines-distance="150"
      :move-speed="2"
      :hover-effect="true"
      hover-mode="grab"
      :click-effect="false"
    />
    <v-container class="fill-height warpper" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>登录</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="loginForm" v-model="valid">
                <v-text-field
                  v-model="loginForm.username"
                  :rules="rules.usernameRules"
                  label="用户名"
                  name="login"
                  prepend-icon="mdi-account"
                  type="text"
                />
                <v-text-field
                  id="password"
                  label="密码"
                  name="password"
                  prepend-icon="mdi-lock"
                  v-model="loginForm.password"
                  :rules="rules.passwordRules"
                  :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show ? 'text' : 'password'"
                  @click:append="show = !show"
                />
              </v-form>
              <!--<v-alert type="success">I'm a success alert.</v-alert>-->
            </v-card-text>
            <v-alert v-if="invalid" dense outlined type="error">
              {{ errorMsg }}
            </v-alert>
            <v-card-actions>
              <v-spacer />
              <v-btn @click="submitForm" color="primary"> 登录 </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import md5 from "@/utils/md5.js";
export default {
  name: "Register",
  data() {
    return {
      curYear: 0,
      show: false,
      show2: false,
      isWaiting: false,
      loginForm: {
        username: "",
        password: "",
      },
      invalid: false,
      errorMsg: "",
      rules: {
        usernameRules: [
          (v) => !!v || "请输入用户名",
          (v) => (v && v.length >= 3) || "用户名长度必须大于2",
          (v) => (v && v.length <= 16) || "用户名长度必须小于等于16",
          (v) => /[a-zA-Z0-9_\u4e00-\u9fa5]+/.test(v) || "非法用户名",
        ],
        passwordRules: [
          (v) => !!v || "请输入密码",
          (v) => (v && v.length >= 8) || "密码长度必须大于等于8",
        ],
      },
    };
  },
  created() {
    this.curYear = new Date().getFullYear();
  },
  methods: {
    ...mapActions("user", ["LoginIn"]),
    submitForm() {
      if (this.$refs.loginForm.validate()) {
        var subForm = JSON.parse(JSON.stringify(this.loginForm));
        subForm.password = md5(subForm.password);
        const res = this.LoginIn(subForm);
        res
          .then((code) => {
            console.log(code);
            // alert("登陆成功!");
            this.$router.push({ name: "Home" });
          })
          .catch((error) => {
            this.invalid = true;
            this.errorMsg = error;
          });
      }
    },
  },
};
</script>

<style lang="scss">
.warpper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -webkit-transform: translate(-50%, -50%);
  display: flex;
}
</style>
