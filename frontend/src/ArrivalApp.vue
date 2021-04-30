<template>
  <v-app>
    <NavigationBar :selectedItem="0" />
    <AppBar />
    <Arrival />
    <!-- <Footer /> -->
  </v-app>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'
import AppBar from './components/AppBar.vue'
// import Footer from "./components/Footer.vue";
import Arrival from './components/Arrival.vue'
import './assets/custom.css'

export default {
  name: 'app',
  components: {
    NavigationBar,
    AppBar,
    // Footer,
    Arrival
  }
}
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
