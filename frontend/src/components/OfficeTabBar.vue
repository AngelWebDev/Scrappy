<template v-slot:extension>
  <v-container no-gutters>
    <h1 class="tab-title text-left">{{ $t("side-bar.office") }}</h1>
    <v-tabs align-with-title v-model="tab">
      <v-tab v-for="item in items" :key="item.title">{{
        $t(`office.${item.title}`)
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
import Users from "./office/Users";
import Customers from "./office/Customers";
import Reports from "./office/Reports";
export default {
  name: "office-tab-bar",
  components: {
    Users,
    Customers,
    Reports,
  },
  data() {
    return {
      tab: null,
      items: [
        { title: "users", content: "Users" },
        { title: "customers", content: "Customers" },
        { title: "reports", content: "Reports" },
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
</style>
