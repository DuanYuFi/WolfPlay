<template>
  <div>
    <h1 style="padding-left: 7%">Profile</h1>
    <template v-if="edit">
      <v-container id="user-profile" fluid tag="section">
        <v-row style="height: 56px" />
        <v-row justify="center">
          <v-col cols="12" md="8">
            <BaseCard color="#283333">
              <template v-slot:heading>
                <div class="display-2 font-weight-light">Edit Profile</div>
                <div class="subtitle-1 font-weight-light">
                  Complete your profile
                </div>
              </template>

              <v-form>
                <v-container class="py-0">
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        label="Email Address"
                        class="purple-input"
                      />
                    </v-col>
                    <v-col cols="12">
                      <v-text-field class="purple-input" label="User Name" />
                    </v-col>

                    <v-col cols="12">
                      <v-text-field
                        label="Old Password"
                        class="purple-input"
                        type="passowrd"
                      />
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        label="New Password"
                        class="purple-input"
                        type="passowrd"
                      />
                    </v-col>
                    <v-col cols="12" class="text-right">
                      <v-btn color="#00bcd4" class="mr-0">
                        Update Profile
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
            </BaseCard>
          </v-col>
        </v-row>
      </v-container>
    </template>
    <template v-else>
      <v-form>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userInfo.username"
                label="UserName"
                outlined
                readonly
                color="#888888"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="userInfo.email"
                label="E-Mail"
                outlined
                readonly
                color="#888888"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
      <v-row>
        <v-col offset-md="5">
          <v-btn @click: append="edit = true">更改个人信息</v-btn>
        </v-col>
      </v-row>
    </template>
  </div>
  <!--
  <v-form>
  <v-container>
      <v-row>
        <v-col cols="12" sm="6">
          <v-text-field
            value="username"
            label="UserName"
            outlined
            readonly
            color = "#888888"
          ></v-text-field>
        </v-col>
      </v-row> 
      <v-row> 
       <v-col cols="12" sm="6">
          <v-text-field
            value="John Doe"
            label="Outlined"
            outlined
            readonly
            color = "#888888"
          ></v-text-field>
        </v-col>
      </v-row>
  </v-container>
  </v-form>
-->
</template>

<script>
import { mapGetters } from "vuex";
// import BaseCard from "@/components/baseCard.vue";
export default {
  data: () => ({
    username: "test",
    email: "test.test",
    edit: false,
  }),
  components: {
    // BaseCard,
  },
  computed: {
    ...mapGetters("user", ["userInfo"]),
  },
  methods: {
    debug() {
      console.log(this.userInfo);
    },
  },
};
</script>

<style>
</style>
