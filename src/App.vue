<template>
  <v-app>
    <Bar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import Bar from "./components/bar";

export default {
  name: "App",
  components: {
    Bar,
  },
  data: () => ({
    //
  }),
  created() {
    this.$vuetify.theme.dark = true;
    // this.$vuetify.theme.themes.dark.anchor = "#333333";
  },
};
</script>
