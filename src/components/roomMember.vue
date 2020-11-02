<template>
  <v-list subheader>
    <v-subheader>Room Members</v-subheader>
    <v-list-item avatar v-for="(chat, Username) in chats" v-bind:key="chat.name" :to="/chat/ + Username">
      <v-list-item-content>
        <v-list-item-title v-html="chat.name"></v-list-item-title>
      </v-list-item-content>
      <v-list-item-action>
        <v-icon>mdi-chat</v-icon>
      </v-list-item-action>
    </v-list-item>
  </v-list>
</template>

<script>
  export default{
    created () {
      this.$store.dispatch('loadUserChats')
    },
    computed: {
      chats () {
        return this.$store.getters.members
      }
    }
  }
</script>
