<template>
  <v-app-bar absolute flat color="white" elevate-on-scroll>
    <v-container class="grey lighten-5">
      <v-row no-gutters class="mt-16 pt-4">
        <v-col cols="8" class="pt-2">
          {{ nowTime }}
        </v-col>
        <v-col cols="3" class="text-right pr-4 pt-2">
          {{ $t("app-bar.logged-in-user") }}:
          <strong>{{ user.firstname + " " + user.lastname }}</strong>
        </v-col>
        <v-col class="text-right " cols="1" sm="1">
          <v-select
            v-model="locale"
            :items="lans"
            dense
            outlined
            @change="selectLanguage"
          ></v-select>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12">
          <p class="p-0 ma-0 text-right">
            <a href="/logout">{{ $t("app-bar.logout") }}</a>
          </p>
          <p class="p-0 ma-0 text-right">
            <a href="/password_change">{{ $t("app-bar.change-password") }}</a>
          </p>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
import moment from "moment";
export default {
  name: "app-bar",
  components: {},
  data() {
    return {
      items: [
        { title: "Arrival", icon: "mdi-dolly" },
        { title: "Payout", icon: "mdi-credit-card-outline" },
        { title: "Office", icon: "mdi-office-building" },
      ],
      lans: process.env.VUE_APP_I18N_SUPPORTED_LOCALE.split(","),
      locale: "en",
      right: null,
      user: {},
      nowTime: "",
    };
  },
  created() {
    // eslint-disable-next-line no-undef
    this.user = authUser;
  },
  mounted() {
    this.nowTimes();
  },
  methods: {
    selectLanguage() {
      if (this.$i18n.locale !== this.locale) {
        this.$i18n.locale = this.locale;
      }
    },
    nowTimes() {
      this.nowTime = moment(new Date()).format("MM-DD-YYYY hh:mm");
      setTimeout(this.nowTimes, 30 * 1000);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-app-bar {
  margin-left: 260px;
}
</style>
