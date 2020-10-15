<template>
  <div class="title">
    <h1>{{ userInfo }}</h1>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Test",
  data() {
    return {

    }
  },
  computed: {
    ...mapGetters("user", ["userInfo", "token"]),
  },
}
</script>

<style lang = "scss">
.title {
  text-align: center;
}
</style>