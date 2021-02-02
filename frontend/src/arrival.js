import Vue from 'vue';
import App from './ArrivalApp.vue';
import Vuex from "vuex";
import vuetify from './plugins/vuetify'

Vue.use(Vuex)
Vue.config.productionTip = false;

const store = new Vuex.Store({
  state: {
    count: 12
  },
  mutations: {
    increment (state) {
      state.count++
    },
    decrement (state) {
      state.count++
    }
  }
})

new Vue({
  vuetify,
  store,
  render: h => h(App),
}).$mount('#app')
