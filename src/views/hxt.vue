<template>
  <div>
      <h1 style = "text-align: center;">I Love You</h1>
      <br/>
    <v-card class="mx-auto" max-width="500">
      <v-img
        class="white--text align-end"
        height="360px"
        src="../assets/hxt.jpg"
      >
      </v-img>

      <v-card-subtitle class="pb-0">Oct 16</v-card-subtitle>

      <v-card-text class="text--primary">
        <div>HXT and her baby</div>

        <div>In Heze, Shandong, China</div>
      </v-card-text>

      <v-card-actions>
        <v-btn color="orange" text> Share </v-btn>

        <v-btn color="orange" text> Explore </v-btn>
        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-heart</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-bookmark</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-share-variant</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => {},
};
</script>