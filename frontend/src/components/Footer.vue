<template>
  <v-container class="grey lighten-5">
    {{ Header }}
  </v-container>
</template>

<script>
export default {
  name: "footer",
  components: {},
  data() {
    return {
      Header: "Footer",
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-app-bar {
  margin-left: 260px;
}
</style>
