import Vue from "vue";
import App from "./OfficeApp.vue";
import Vuex from "vuex";
import vuetify from "./plugins/vuetify";
import i18n from "./i18n";

Vue.use(Vuex);
Vue.config.productionTip = false;

const store = new Vuex.Store({
  state: {
    users: 12,
  },
  mutations: {
    increment(state) {
      state.count++;
    },
    decrement(state) {
      state.count++;
    },
  },
});

new Vue({
  vuetify,
  i18n,
  store,
  render: (h) => h(App),
}).$mount("#app");
