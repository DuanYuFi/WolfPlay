<template>
  <div>
    <div class="message" v-for="(message,index) in messages" v-bind:key="index" :class="{own: message.user == username}">
      <div class="username" v-if="index>0 && messages[index-1].user != message.user">{{message.user}}</div>
      <div class="username" v-if="index == 0">{{message.user}}</div>
      <div style="margin-top: 5px"></div>
      <div class="content">
        <div v-html="message.content"></div>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    data () {
      return {}
    },
    props: [
      'messages'
    ],
    computed: {
      username () {
        return this.$store.getters.userInfo.username
      }
    },
  }
</script>

<style>
  span.emoji {
    font-size: 20px;
    vertical-align: middle;
    line-height: 2;
  }
</style>
