<template v-slot:extension>
  <v-container fluid class="arrival_container">
    <h1 class="tab-title text-left">{{ $t("side-bar.arrival") }}</h1>
    <v-row>
      <v-col cols="6">
        <v-autocomplete
          v-model="value"
          :items="customers"
          outlined
          dense
          chips
          small-chips
          label="Outlined"
        />
      </v-col>
      <v-col cols="6">
        <v-label>name</v-label>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "arrival",
  components: {},
  data() {
    return {
      customers: ["foo", "bar", "fizz", "buzz"],
      customer: {
        id: null,
        name: null,
        street: null,
        zip: null,
        city: null,
        company: {},
      },
      value: "",
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.arrival_container {
  width: calc(100% - 260px);
  margin-top: 140px;
  margin-left: 260px;
}
</style>
