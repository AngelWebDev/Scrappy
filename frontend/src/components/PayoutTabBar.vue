<template v-slot:extension>
  <v-container no-gutters>
    <h1 class="tab-title text-left">{{ $t("side-bar.payout") }}</h1>
    <v-tabs align-with-title v-model="tab">
      <v-tab v-for="item in items" :key="item.title">{{
        $t(`payout.${item.title}`)
      }}</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in items" :key="item.title">
        <component v-bind:is="item.content"></component>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import Open from "./payout/Open";
import Paid from "./payout/Paid";
export default {
  name: "payout-tab-bar",
  components: {
    Open,
    Paid,
  },
  data() {
    return {
      tab: null,
      items: [
        { title: "open", content: "Open" },
        { title: "paid", content: "Paid" },
      ],
      right: null,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-tabs {
  margin-left: 220px;
  margin-top: 10px;
  margin-bottom: 20px;
}
.tab-title {
  margin-left: 260px;
  margin-top: 150px;
  padding-left: 20px;
}
.v-window {
  overflow: visible !important;
}
</style>
