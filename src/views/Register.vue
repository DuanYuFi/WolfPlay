<template>
  <div class="register">
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
              <v-toolbar-title>注册</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="registerForm" v-model="valid">
                <v-text-field
                  v-model="registerForm.username"
                  :rules="rules.usernameRules"
                  label="用户名"
                  name="login"
                  prepend-icon="mdi-account"
                  type="text"
                  @change="invalid = false"
                />
                <v-text-field
                  id="password"
                  label="密码"
                  name="password"
                  prepend-icon="mdi-lock"
                  v-model="registerForm.password"
                  :rules="rules.passwordRules"
                  :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show ? 'text' : 'password'"
                  @click:append="show = !show"
                />
                <v-text-field
                  id="rePassword"
                  label="再次输入密码"
                  name="rePassword"
                  prepend-icon="mdi-lock-outline"
                  :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show2 ? 'text' : 'password'"
                  v-model="rePassword"
                  :rules="rules.rePasswordRules"
                  @click:append="show2 = !show2"
                />
                <v-text-field
                  v-model="registerForm.email"
                  :rules="rules.emailRules"
                  label="邮箱"
                  name="login"
                  prepend-icon="mdi-email"
                  type="text"
                />
              </v-form>
              <!--<v-alert type="success">I'm a success alert.</v-alert>-->
              <v-alert v-if="invalid" dense outlined type="error">
                用户名已被注册！
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn @click="submitForm" color="primary"> 注册 </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import { register } from "@/api/user";
import md5 from "@/utils/md5.js";
// import { check } from '@/api/user'
export default {
  name: "Register",
  data() {
    return {
      show: false,
      show2: false,
      isWaiting: false,
      rePassword: "",
      registerForm: {
        email: "",
        username: "",
        password: "",
      },
      invalid: false,
      rules: {
        emailRules: [
          (v) => !!v || "请填写邮箱",
          (v) => /.+@.+\..+/.test(v) || "请输入正确的邮箱",
        ],
        usernameRules: [
          (v) => !!v || "请输入用户名",
          (v) => (v && v.length >= 3) || "用户名长度必须大于2",
          (v) => (v && v.length <= 16) || "用户名长度必须小于等于16",
          (v) => /^[a-zA-Z0-9_-]{3,16}$/.test(v) || "非法用户名",
        ],
        passwordRules: [
          (v) => !!v || "请输入密码",
          (v) => (v && v.length >= 8) || "密码长度必须大于等于8",
        ],
        rePasswordRules: [
          (v) => !!v || "请重新输入密码",
          (v) => (!!v && v) === this.registerForm.password || "两次输入不一致",
        ],
      },
    };
  },
  methods: {
    ...mapActions("user", ["LoginIn"]),
    async submitForm() {
      if (this.$refs.registerForm.validate()) {
        var subForm = JSON.parse(JSON.stringify(this.registerForm));
        subForm.password = md5(subForm.password);
        const res = await register(subForm);
        if (res.code === 0) {
          console.log("Success");
          if (res.check == false) {
            this.invalid = true;
          } else {
            this.invalid = false;
            alert("注册成功！");
            this.$router.push({ name: "Login" });
          }
        }
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
