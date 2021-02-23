<template v-slot:extension>
  <v-container fluid class="arrival_container">
    <h1 class="tab-title text-left pb-16">{{ $t("side-bar.arrival") }}</h1>
    <v-row>
      <v-col cols="5">
        <v-autocomplete
          v-model="form.customer"
          :items="customers"
          outlined
          dense
          chips
          small-chips
          :label="$t('table-data.customer')"
        />
        <v-select
          dense
          :items="materials"
          v-model="form.material"
          :label="$t('table-data.material')"
          outlined
        />
        <v-text-field
          dense
          :label="$t('table-data.weight')"
          v-model="form.weight"
          outlined
          suffix="kg"
        />
      </v-col>
      <v-col cols="7" class="text-left pr-12">
        <v-simple-table v-if="customer.id === null">
          <template v-slot:default>
            <tbody>
              <tr>
                <td>{{ $t("table-data.name") }}:</td>
                <td>{{ customer.name }}</td>
              </tr>
              <tr>
                <td>{{ $t("table-data.company") }}:</td>
                <td>{{ customer.name }}</td>
              </tr>
              <tr>
                <td>{{ $t("table-data.address") }}:</td>
                <td>{{ customer.name }}</td>
              </tr>
              <tr>
                <td>
                  {{ $t("table-data.zip") }} / {{ $t("table-data.city") }}:
                </td>
                <td>{{ customer.name }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-btn depressed>
          {{ $t("form-data.clear") }}
        </v-btn>
      </v-col>
      <v-col cols="6">
        <v-btn depressed color="primary">
          {{ $t("form-data.save") }}
        </v-btn>
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
      materials: ["Cooper", "Iron", "Wood", "Ceramics"],
      form: {
        customer: {},
        material: "Cooper",
        weight: 0,
      },
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
  padding: 30px;
}
</style>
