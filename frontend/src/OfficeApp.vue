<template>
  <v-app>
    <NavigationBar :selectedItem="2" />
    <AppBar />
    <OfficeTabBar />
    <!-- <Footer /> -->
  </v-app>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue";
import AppBar from "./components/AppBar.vue";
import OfficeTabBar from "./components/OfficeTabBar.vue";
// import Footer from "./components/Footer.vue";
import "./assets/custom.css";

export default {
  name: "app",
  components: {
    NavigationBar,
    AppBar,
    OfficeTabBar,
    // Footer,
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
